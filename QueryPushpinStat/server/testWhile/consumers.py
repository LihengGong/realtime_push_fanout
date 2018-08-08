from channels.generic.websocket import WebsocketConsumer
import json
from .getstats import read_stats_block


class StatConsumer(WebsocketConsumer):
    def connect(self):
        print('in StatConsumer.connect')
        self.accept()
        print('StatConsumer: ready to connect to Pushpin socket')
        read_stats_block()

    def disconnect(self, close_code):
        print('StatConsumer: websocket disconnected; close code: ', close_code)

    def receive(self, text_data):
        # TODO: add real receive code here
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('in StatConsumer.receive')

        self.send(text_data=json.dumps({
            'message': message
        }))

    # "def send(self, text_data=None, bytes_data=None, close=False):"
    def send(self, bytes_data):
        # TODO: add real send code here
        print('in StatConsumer.send')
