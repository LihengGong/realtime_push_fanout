from channels.generic.websocket import WebsocketConsumer
import json


class StatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # TODO: add real receive code here
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

    # "def send(self, text_data=None, bytes_data=None, close=False):"
    def send(self, bytes_data):
        # TODO: add real send code here
        pass
