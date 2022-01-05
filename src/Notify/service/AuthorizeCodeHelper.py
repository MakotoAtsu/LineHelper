import httpx


token_url = 'https://notify-bot.line.me/oauth/token'
client_id = 'VpvEjfLIcrwNEPq6Px3NVZ'
client_secret = '0OHgrhwcv8GhELDaNohMhAjFuVwC5s6JCpfgwN1tQea'
room_info_uri = 'https://notify-api.line.me/api/status'
revoke_token_uri = 'https://notify-api.line.me/api/revoke'
line_oauth_url = 'https://notify-bot.line.me/oauth/authorize'

redirect_uri = 'http://line.pixis.com.tw:8000/AuthorizeCode'


class AuthorizeCodeHelper:

    def get_line_notify_access_token(self, code: str):

        response = httpx.post(token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
        })

        if response.status_code is not 200:
            return None

        return response.json()

    def get_notify_room_info(self, token: str):

        resp = httpx.get(room_info_uri, headers={
            'Authorization': f'Bearer {token}'
        })

        if resp.status_code is not 200:
            return None

        return resp.json()

    def revoke_token(self, token: str) -> None:
        httpx.post(revoke_token_uri, headers={
            'Authorization': f'Bearer {token}'
        })

    @staticmethod
    def get_generate_line_notify_url(uuid: str):

        url = f'{line_oauth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=notify&state={uuid}&response_mode=query'
        return url
