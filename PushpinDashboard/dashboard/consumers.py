import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.consumer import AsyncConsumer
# from channels.layers import get_channel_layer
from .tasks import read_stats_block
from .models import PushpinStatConn, Clients


# websocket close code list
"""
Close code (uint16)	Codename	Internal	Customizable	Description
0-999	-	Yes	No	Unused
1000	CLOSE_NORMAL	No	No	Successful operation, regular socket shutdown
1001	CLOSE_GOING_AWAY	No	No	One of the socket endpoints is exiting
1002	CLOSE_PROTOCOL_ERROR	No	No	Error in one of the endpoints while processing a known message type
1003	CLOSE_UNSUPPORTED	No	No	Endpoint received unsupported data type (text/binary)
1004	-	Yes	No	Unused
1005	CLOSED_NO_STATUS	Yes	No	Expected close status, received none
1006	CLOSE_ABNORMAL	    Yes	No	No close code frame has been receieved
1007	Unsupported Data	No	No	Endpoint received inconsistent message (e.g. non-UTF8 data within a string)
1008	Policy Violation	No	No	Endpoint policy was violated, is a generic code used when codes 1003 and 1009 aren't suitable
1009	CLOSE_TOO_LARGE	No	No	Data frame size is too large
1010	Missing Extension	No	No	Client asked for extension that server didn't reply with
1011	Internal Error	No	No	Internal server error while operating
1012	Service Restart	No	No	Server/service is restarting
1013	Server Overload/Try Again Later	No	No	Try Again Later code; temporary server condition forced to block client's request
1014	-	Yes	No	Unused; reserved for later
1015	TLS Handshake Fail	Yes	No	TLS handshake failure
1016-1999	-	Yes	No	Reserved for later
2000-2999	-	Yes	No	Reserved for websocket extensions
3000-3999	-	Yes	Yes	Reserved for frameworks, can be registered at IANA
4000-4999	-	No	Yes	Available for applications
"""
stat_group = None

"""
class StatConsumer(WebsocketConsumer):
    def connect(self):
        Clients.objects.all().delete()
        Clients.objects.create(channel_name=self.channel_name)
        print('Clients count is: ', Clients.objects.count())
        print('connect: channel_name=', self.channel_name)
        # async_to_sync(self.channel_layer.group_add)("stat_group", self.channel_name)
        self.accept()
        read_stats_block()

    def disconnect(self, close_code):
        print('StatConsumer: websocket disconnected; close code: ', close_code)
        # TODO: Error handling
        if close_code >= 1002:
            print('Error! Something is wrong!')
        Clients.objects.filter(channel_name=self.channel_name).delete()

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            "stat_group",
            {
                "type": "stat.message",
                "text": "hello",
            },
        )
        # TODO: add real receive code here
        print('in StatConsumer.receive, text_data: ', text_data)
        send_data = None
        if text_data == 'get_conn':
            send_data = ''
            for obj in PushpinStatConn.objects.all():
                print('cur obj is: ', obj)
                send_data += str(obj)
        # self.send('from server')

        if send_data:
            self.send(text_data=json.dumps({
                'message': send_data
            }))

    def stat_message(self, event):
        print('in consumer: stat_message')
        self.send(text_data=event['text'])

    # "def send(self, text_data=None, bytes_data=None, close=False):"
    def send1(self, bytes_data):
        # TODO: to be modified. Placeholder now
        print('in StatConsumer.send')
"""


class StatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Connected')
        print(event)
        print(self.channel_name)
        Clients.objects.all().delete()
        Clients.objects.create(channel_name=self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })
        print('ready to launch celery task to get pushpin status')
        # launch celery asynchronous task
        read_stats_block.delay()
        print('celery task has been fired')

    async def websocket_receive(self, event):
        print("Received")
        print(event)
        await self.send('send')

    async def stat_message(self, event):
        print('in stat_message')
        print(event)
        await self.send({
            "type": "websocket.send",
            "text": event["text"],
        })
