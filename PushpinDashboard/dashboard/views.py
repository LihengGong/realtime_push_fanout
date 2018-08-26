from django.shortcuts import render, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import status
from .models import Clients
# from .consumers import StatConsumer


# Create your views here.
def send_msg(request):
    channel_layer = get_channel_layer()
    print('send_msg: before sending:', channel_layer)
    # channel_layer.send("channel_name", {
    #     "type": "stat.message",
    #     "text": 'hello'
    # })
    # channel_name = None
    try:
        channel_name = Clients.objects.all()[:1].get().channel_name
    except ObjectDoesNotExist:
        print('No channels right now')
        return HttpResponse('no channels', status=status.HTTP_400_BAD_REQUEST)
    if channel_name:
        print('send_msg: channel_name=', channel_name)
    async_to_sync(channel_layer.send)(channel_name, {'type': 'stat.message', 'text': 'data'})
    print('send_msg: after sending...')
    return HttpResponse('Done')
