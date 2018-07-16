from urlparse import urlparse
import json
from functools import wraps
import django.test.client
from gripcontrol import Channel, HttpResponseFormat, WebSocketMessageFormat
from django.http import HttpResponse, HttpResponseBadRequest
from django_grip import set_hold_longpoll, publish

WAIT_MAX = 60 * 5

class Checkpoint(object):
	def __init__(self, etag=None, changes_link=None):
		self.etag = None
		self.changes_link = None

class ResourceInfo(object):
	def __init__(self):
		self.uri = None
		self.etag = None
		self.changes_link = None
		self.empty = False

# TODO: add args for type, get_items_func
def live(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		return view_func(*args, **kwargs)
	wrapper.live = True
	return wrapper

# GET request only. meta must contain headers using "HTTP_{header.upper}" format
def internal_request(path, meta=None):
	client = django.test.client.Client()
	kwargs = dict()
	if meta:
		for k, v in meta.iteritems():
			if k.startswith('HTTP_'):
				kwargs[k] = v
	kwargs['HTTP_INTERNAL'] = '1'
	return client.get(path, {}, **kwargs)

def canonical_uri(uri):
	result = urlparse(uri)
	return result.path

def parse_header_params(value):
	parts = value.split(';')
	first = parts.pop(0)
	params = dict()
	for part in parts:
		k, v = part.lstrip().split('=', 1)
		params[k] = v
	return (first, params)

def get_link(response, rel):
	link_headers = response.get('Link')
	if link_headers:
		link_headers = link_headers.split(',')
		for link_header in link_headers:
			link, params = parse_header_params(link_header)
			if params.get('rel') == rel:
				if len(link) < 3 or link[0] != '<' or link[-1] != '>':
					raise ValueError('bad link format')
				return link[1:-1]
	return None

# return None if the response doesn't seem to be LiveResource compatible
def get_resourceinfo(uri, response):
	etag = None
	if 'ETag' in response:
		etag = response.get('ETag')

	changes_link = get_link(response, 'changes')

	if etag or changes_link:
		ri = ResourceInfo()
		ri.uri = uri
		if etag:
			ri.etag = etag
			if response.status_code == 304:
				ri.empty = True
		if changes_link:
			ri.changes_link = changes_link
			if response.status_code == 200 and len(response.content > 0):
				items = json.loads(response.content)
				if len(items) == 0:
					ri.empty = True
		return ri

	return None

# modes: value, changes, value-multi, changes-multi
def channel_for_uri(uri, mode):
	return 'lr-%s-%s' % (mode, uri)

def channel_object_for_request(request, resourceinfo, multi=False):
	if request.META.get('HTTP_IF_NONE_MATCH') and resourceinfo.etag:
		mode = 'value'
		prev_id = resourceinfo.etag
	elif resourceinfo.changes_link:
		mode = 'changes'
		prev_id = resourceinfo.changes_link
	else:
		raise ValueError('bad resource format')

	if multi:
		mode = mode + '-multi'

	channel_name = channel_for_uri(resourceinfo.uri, mode)

	return Channel(channel_name, prev_id=prev_id)

# hijack requests and be able to make internal requests
class LiveResourceMiddleware(object):
	def process_view(self, request, view_func, view_args, view_kwargs):
		# require grip middleware
		assert hasattr(request, 'grip_proxied'), 'GripMiddleware must run before LiveResourceMiddleware'

		if getattr(view_func, 'live', False):
			# parse wait header
			wait = request.META.get('HTTP_WAIT')
			if wait is not None:
				try:
					wait = int(wait)
				except:
					return HttpResponseBadRequest('Invalid Wait header specified.\n')

				if wait < 1:
					wait = None
				elif wait > WAIT_MAX:
					wait = WAIT_MAX

			resp = view_func(request, *view_args, **view_kwargs)

			if wait:
				if not request.grip_proxied:
					return HttpResponse('Error: Realtime request not supported. Set up Pushpin or Fanout.\n', status=501)

				if hasattr(resp, 'multi_info'):
					channels = list()
					for ri in resp.multi_info:
						try:
							channel = channel_object_for_request(request, ri, True)
						except:
							return HttpResponse('Resource cannot be used for updates.\n', status=501)
						channels.append(channel)
					set_hold_longpoll(resp, channels, timeout=wait)
				else:
					ri = get_resourceinfo(canonical_uri(request.path), resp)
					if ri:
						try:
							channel = channel_object_for_request(request, ri, True)
						except:
							return HttpResponse('Resource cannot be used for updates.\n', status=501)
						set_hold_longpoll(resp, channel, timeout=wait)

			return resp

def updated(uri, prev_checkpoint=None):
	uri = canonical_uri(uri)

	resp = internal_request(uri)
	resp_headers = dict()
	for k, v in resp.items():
		resp_headers[k] = v

	if len(resp.content) > 0:
		try:
			resp_body = json.loads(resp.content)
		except:
			resp_body = ''
	else:
		resp_body = ''

	msg = dict()
	msg['type'] = 'event'
	msg['uri'] = uri
	msg['headers'] = resp_headers
	msg['body'] = resp_body

	formats = list()
	formats.append(HttpResponseFormat(code=resp.status_code, headers=resp_headers, body=resp.content))
	formats.append(WebSocketMessageFormat(json.dumps(msg)))

	channel = channel_for_uri(uri, 'value')

	# TODO: id, prev_id
	publish(channel, formats)

	# TODO: publish changes, value-multi, and changes-multi?
