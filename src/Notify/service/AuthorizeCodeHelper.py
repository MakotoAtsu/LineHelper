import httpx


token_url = 'https://notify-bot.line.me/oauth/token'
client_id = 'VpvEjfLIcrwNEPq6Px3NVZ'
client_secret = '0OHgrhwcv8GhELDaNohMhAjFuVwC5s6JCpfgwN1tQea'
redirect_uri = 'https://447f-180-217-5-131.ngrok.io/AuthorizeCode'

room_info_uri = 'https://notify-api.line.me/api/status'


class AuthorizeCodeHelper:

    async def get_line_notify_access_token(self, code: str):

        response = httpx.post(token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        })

        print(type(response.json()))
        return response.json()

    async def get_notify_room_info(self, token: str):

        resp = httpx.get(room_info_uri, headers={
            'Authorization': f'Bearer {token}'
        })

        print(resp.json())
        return resp.json()
