from os import stat
from django.http import HttpResponse, HttpRequest, JsonResponse
from asgiref.sync import async_to_sync
from django.views.generic.base import View
from Notify.service.AuthorizeCodeHelper import AuthorizeCodeHelper
from Notify.service.ChannelService import ChannelService
import json


# Create your views here.

class AuthorizeCode(View):
    def get(self, request: HttpRequest):

        # Step.1 從 QueryString 取得 AuthorizeCode 與 State
        query_str = request.GET
        code = query_str.get('code', '')
        state = query_str.get('state', '')

        if (not code or not state):
            return HttpResponse(f'Invalid Request')

        # Step.2 使用 AuthorizeCode 取回 Access Token
        service = AuthorizeCodeHelper()
        token_response = service.get_line_notify_access_token(code)

        if not token_response:
            return HttpResponse(f'Cannot get room access token...')

        access_token = token_response['access_token']

        # Step.3 使用 Access Token 取回聊天室資訊
        room_info = service.get_notify_room_info(access_token)

        if not room_info:
            service.revoke_token(access_token)
            return HttpResponse(f'Cannot get room info...')

        data = {
            "Code": code,
            'State': state,
            'Result': token_response,
            'Client_id': state,
            'Token': access_token,
            'Room': {
                'Type': room_info['targetType'],
                'Name': room_info['target']
            }
        }

        print(data)
        # Step.4 檢查是否已有 Client 連入 Channel
        target_client = ChannelService.ws_client.get(state, None)
        if (target_client):
            target_client.send(json.dumps(data, ensure_ascii=False))

        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
