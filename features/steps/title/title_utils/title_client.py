import json

from tools.logger import GetLogger
log=GetLogger().get_logger()


from features.steps.api.api_utils.requests_session import RequestsSession
from urllib.parse import quote


class TitleClient:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)

    def create_title(self,token,name='',source_id=''):
        '''创建title'''
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        log.info('请求header为{}'.format(header))
        data = {
            "name": name,
            "source_id": source_id
        }

        return self._session.post(
            'api/v1/title/create',
            json=data,
            headers=header
        )

    def query_movies(self,token,search_text):
        return self._session.get(
            'api/v1/title/movies' + '?search_text=' + search_text,
            headers={'X-Thunderstorm-Key': token}
        )

    def query_title_by_str(self, token, search_text='', order_by=''):
        url = 'api/v1/title/titles'
        params={
            'search_text':search_text,
            'order_by':order_by
        }

        return self._session.get(
            url,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )




    def query_title_playlist(self, str_params, token):
        return self._session.get(
            'api/v1/playlist/ppl/by_title' + str_params,
            headers={'X-Thunderstorm-Key': token}
        )

    def query_title_show(self, str_data, token, search_name=None, order_by=None):
        encode = quote(str_data)
        filter = '&filter=' + encode
        path = 'api/v1/schedule/title?page_num=1&page_size=2500' + filter
        if search_name is not None:
            # encode_search = quote(search)
            search = '&search_name=' + search_name
            path += search
        if order_by is not None:
            encode = quote(order_by)
            path += f'&order_by={encode}'
        return self._session.get(
            path,
            headers={'X-Thunderstorm-Key': token}
        )

    def query_title_content(self, title_uuid, token, params=None, filter='', order_by=None):
        if filter != '':
            encode = quote(filter)
            filter = '&filter=' + encode
        path = f'api/v1/content/title/{title_uuid}?page_num=1&page_size=2500' + filter
        # if search_name is not None:
        #     # encode_search = quote(search)
        #     search = '&search_name=' + search_name
        #     path += search
        if order_by is not None:
            encode = quote(order_by)
            path += f'&order_by={encode}'
        return self._session.get(
            path,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )

if __name__ == '__main__':

    from features.setup import producer_login
    from features.constants import PRODUCER2_URI, PRODUCER2_PORTS
    token=producer_login()
    url=PRODUCER2_URI + PRODUCER2_PORTS['title']
    a = TitleClient(url).create_title(token,'')
    # a=TitleClient(url).query_title_by_str('未来福音',token)

    print(a.json())