from channels.generic.websocket import WebsocketConsumer

import json
import logging

logger = logging.getLogger('django')

class NotifyConsumer(WebsocketConsumer):
    def connect(self):
        self.name : str = self.scope['url_route']['kwargs']['name']
        self.accept()
        print('===================AAAAAAAAAAAA========================')
        logging.debug(f'Connect : {self.name}')
        return super().connect()


    def disconnect(self, code):
        return super().disconnect(code)


    def receive(self, text_data= None):
        text_data_json = json.loads(text_data)
        message = self.name + ': ' + text_data_json['message']
        logger.debug('send')

        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
