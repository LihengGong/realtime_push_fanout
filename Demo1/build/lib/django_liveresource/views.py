from copy import deepcopy
import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django_grip import websocket_only
from django_liveresource import internal_request, canonical_uri, parse_header_params, channel_for_uri, get_resourceinfo

class WsRequestError(Exception):
	def __init__(self, condition, message=''):
		super(WsRequestError, self).__init__(message)
		self.condition = condition

def _handle_ws_request(ws, req):
	rtype = req.get('type')
	if rtype is None or not isinstance(rtype, basestring) or rtype not in ('subscribe', 'unsubscribe', 'ping'):
		raise WsRequestError('unknown-type')

	if rtype == 'ping':
		return {'type': 'pong'}

	# if we are here, then the type is subscribe or unsubscribe
	assert(rtype == 'subscribe' or rtype == 'unsubscribe')

	uri = req.get('uri')
	if uri is None or not isinstance(uri, basestring):
		raise WsRequestError('bad-request')

	try:
		uri = canonical_uri(uri)
	except:
		raise WsRequestError('bad-request')

	mode = req.get('mode')
	if mode is None or not isinstance(mode, basestring) or mode not in ('value', 'changes'):
		raise WsRequestError('bad-request')

	if rtype == 'subscribe':
		ws.subscribe(channel_for_uri(uri, mode))
		return {'type': 'subscribed'}
	else: # unsubscribe
		ws.unsubscribe(channel_for_uri(uri, mode))
		return {'type': 'unsubscribed'}

def multi(request):
	if request.method != 'GET':
		return HttpResponseNotAllowed(['GET'])

	# prevent loops
	if request.META.get('HTTP_INTERNAL') == '1':
		return HttpResponseBadRequest('Can\'t make internal requests to the multi resource.\n')

	# headers to pass along
	headers_meta = dict()
	for k, v in request.META.iteritems():
		if k not in ('HTTP_INTERNAL', 'HTTP_WAIT'):
			headers_meta[k] = v

	uri_headers = dict()
	for i in request.META.get('HTTP_URI').split(','):
		try:
			uri, params = parse_header_params(i)
		except:
			return HttpResponseBadRequest('Failed to parse Uri header.\n')

		try:
			uri = canonical_uri(uri)
		except:
			return HttpResponseBadRequest('Invalid Uri value.\n')

		uri_headers[uri] = params

	info = list()
	results = dict()
	for uri, params in uri_headers.iteritems():
		meta = deepcopy(headers_meta)
		for k, v in params.iteritems():
			meta['HTTP_' + k.upper()] = v

		resp = internal_request(uri, meta)

		ri = get_resourceinfo(resp, uri)
		if ri and ri.empty:
			info.append(ri)
			continue

		resp_headers = dict()
		for k, v in resp.items():
			resp_headers[k] = v

		try:
			resp_body = json.loads(resp.content)
		except:
			return HttpResponseBadRequest('One or more resources produces non-JSON content.\n')

		result = dict()
		result['code'] = resp.status_code
		result['headers'] = resp_headers
		result['body'] = resp_body

		results[uri] = result

	resp = HttpResponse(json.dumps(results), content_type='application/json')

	# to help out the middleware, provide list of ResourceInfo if the response would be empty
	resp.multi_info = info if len(results) == 0 else []
	return resp

@websocket_only
def updates(request):
	ws = request.wscontext

	# accept all incoming connections
	if ws.is_opening():
		ws.accept()

	while ws.can_recv():
		message = ws.recv()
		if message is None:
			ws.close()
			break

		# each incoming message must be a JSON object containing an id field,
		#   otherwise we consider it bad protocol and close the connection

		try:
			req = json.loads(message)
		except:
			resp = {'type': 'error', 'condition': 'bad-protocol'}
			ws.send(json.dumps(resp))
			ws.close()
			break

		rid = req.get('id')
		if rid is None or not isinstance(rid, basestring):
			resp = {'type': 'error', 'condition': 'bad-protocol'}
			ws.send(json.dumps(resp))
			ws.close()
			break

		try:
			resp = _handle_ws_request(ws, req)
		except WsRequestError as e:
			resp = {'type': 'error', 'condition': e.condition}
		except:
			resp = {'type': 'error', 'condition': 'internal-server-error'}

		resp['id'] = rid

		ws.send(json.dumps(resp))
