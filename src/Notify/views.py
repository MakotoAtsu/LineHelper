from os import stat
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
import httpx


# Create your views here.

token_url = 'https://notify-bot.line.me/oauth/token'
client_id = 'VpvEjfLIcrwNEPq6Px3NVZ'
client_secret = '0OHgrhwcv8GhELDaNohMhAjFuVwC5s6JCpfgwN1tQea'


async def received_authorize_code(request: HttpRequest):

    query_str = request.GET

    code = query_str.get('code', '')
    state = query_str.get('state', '')

    if (not code or not state):
        return HttpResponse(f'Invalid Request')

    data = {
        "Code": code,
        'State': state,
        'Result': await get_line_notify_access_token(code, state)
    }

    return JsonResponse(data)


async def get_line_notify_access_token(code: str, state: str):

    response = httpx.post(token_url, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://a143-111-248-245-178.ngrok.io/AuthorizeCode',
        'client_id': client_id,
        'client_secret': client_secret,
        'state': state
    })

    return response.json()


async def Test_PostData(request: HttpRequest):

    response = httpx.get(
        'https://api4.origin.com/xsearch/store/zh_tw/twn/products?searchTerm=&filterQuery=&start=1&rows=1&isGDP=true')

    print(response)
    print(response.json())
    return JsonResponse({})
