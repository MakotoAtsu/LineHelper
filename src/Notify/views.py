from django.http import HttpResponse, HttpRequest, JsonResponse
from asgiref.sync import async_to_sync
from django.views.generic.base import View
from Notify.service.AuthorizeCodeHelper import AuthorizeCodeHelper
from Notify.service.ChannelService import ChannelService

# Create your views here.


def TestSendMsg(req: HttpRequest):

    print("AAAAAAAAA")

    all_clients = [c.clientId for c in ChannelService.ws_client.values()]

    target_client =  ChannelService.ws_client.get('123456',None)
    if (target_client):
        target_client.send_message('HAHA')
    return JsonResponse({
        "Clients": all_clients
    })


class AuthorizeCode(View):
    @async_to_sync
    async def get(self, request: HttpRequest):

        # Step.1 從 QueryString 取得 AuthorizeCode 與 State
        query_str = request.GET
        code = query_str.get('code', '')
        state = query_str.get('state', '')

        if (not code or not state):
            return HttpResponse(f'Invalid Request')

        # Step.2 使用 AuthorizeCode 取回 Access Token
        service = AuthorizeCodeHelper()
        token_response = await service.get_line_notify_access_token(code)

        if (token_response['status'] != 200):
            print(token_response)
            return HttpResponse(f'Cannot get room access token...')

        access_token = token_response['access_token']

        room_info = await service.get_notify_room_info(access_token)

        # Step.3 使用 Access Token 取回聊天室資訊
        

        data = {
            "Code": code,
            'State': state,
            'Result': token_response,
            'token': access_token,
            'room_info': room_info
        }

        return JsonResponse(data)
