from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django_eventstream import send_event
from django_grip import set_hold_stream, publish
from gripcontrol import HttpStreamFormat
from django.core.serializers.json import DjangoJSONEncoder
import json

# Create your views here.
def home(request, room_id=None):
    user = request.GET.get('user')
    context = {}
    context['room_id'] = room_id or 'default'
    if not user:
        if not room_id:
            return redirect('default?' + request.GET.urlencode())
        return render(request, 'chat/join.html', context)
    else:
        context['user'] = user
        return render(request, 'chat/chat.html', context)


def messages(request, room_id):
    if request.method == 'POST':
        mFrom = request.POST['from']
        text = request.POST['text']
        send_event('room-%s' %room_id, 'message', text)
        body = json.dumps(text, cls=DjangoJSONEncoder) + '\n'
        return HttpResponse(body, content_type='application/json')
    else:
        return HttpResponseNotAllowed(['POST'])
