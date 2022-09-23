import json

from features.steps.api.api_utils.requests_session import RequestsSession


class MacroClient:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)

    def create_macro(self, token, data):
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        return self._session.post(
            'api/v1/playlist/macro',
            json=data,
            headers=header
        )

    def query_macro_by_title(self, token, title):
        url = 'api/v1/playlist/macro'
        params = {
            'page_num': 1,
            'page_size': 30,
            'types': [],
            'name': title
        }
        return self._session.get(
            url,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )
