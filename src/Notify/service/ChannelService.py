from channels.generic.websocket import WebsocketConsumer


class ChannelService(WebsocketConsumer):
    ws_client: dict[str, 'ChannelService'] = {}

    def connect(self) -> None:
        """
        客戶端建立連線時,如果需要保持客戶端和伺服器的連結
        self.accept()
        :return: None
        """
        self.uuid: str = self.scope['url_route']['kwargs']['uuid']

        # self.clientId = ''
        self.accept()
        if (self.uuid in ChannelService.ws_client):
            self.disconnect(False)
            return

        ChannelService.ws_client[self.uuid] = self
        print(f'ClientId: {self.uuid} connected')
        print(f'Current Connect amount : {len(ChannelService.ws_client)}')

    def receive(self, text_data=None, bytes_data=None) -> None:
        """
        客戶端發起訊息後 伺服器收到訊息時
        :param text_data:  收到的字串兒資料
        :param bytes_data:  收到的位元組資料二進位制資料流
        :return:  None
        """
        # 業務邏輯,websocket 轉發
        print(f'Client:{self.uuid} - {text_data}')
        self.send('BackEnd Message')

    def disconnect(self, remove_dict: bool = True) -> None:
        """
        客戶端斷開連線
        :param code:斷開的錯誤碼
        :return: None
        """
        if (remove_dict):
            del ChannelService.ws_client[self.uuid]
            print(f'ClientId: {self.uuid} disconnected')
            print(f'Current Connect amount : {len(ChannelService.ws_client)}')

        self.close()
