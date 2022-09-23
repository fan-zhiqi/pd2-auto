#!/usr/bin/python
# -*-coding:utf-8 -*-
from features import constants
from features.steps.api.api_utils.requests_session import RequestsSession
import json


class ShowClient:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)

    def query_show(self, token, match_title_bool='' and bool, search_name='', states=[], start_time='', end_time='',
                   start_date='', screen_show_attributes=[]):
        url = 'api/v1/schedule'
        complex_uuid_list = constants.complex_uuids
        a = {"show_attribute_search_type": 1, 'complex_uuids': complex_uuid_list}
        if states != []:
            a['states'] = states
        if start_time != '':
            a['start_time'] = start_time
        if end_time != '':
            a['end_time'] = end_time
        if match_title_bool != '':
            a['match_title'] = match_title_bool
        if start_date != '':
            a['start_date'] = start_date
        if screen_show_attributes != []:
            a['screen_show_attributes'] = screen_show_attributes

        print(a)
        params = {
            'search_name': search_name,
            'page_num': 1,
            'page_size': 10000,
            'order_by': json.dumps({"start_time": "desc"}),
            'filter': json.dumps(a)
        }
        return self._session.get(
            url,
            params=params,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def match_title(self, token, data):
        url = 'api/v1/title/match_pos'
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        return self._session.post(
            url,
            json=data,
            headers=header
        )

    def unmatch_title(self, token, data):
        url = 'api/v1/title/un_match_pos'
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        return self._session.post(
            url,
            json=data,
            headers=header
        )

    def assigned(self, token, playlist_uuid: str, pos_uuid_list=[]):
        url = 'api/v1/schedule/' + playlist_uuid + '/match_pos'
        data = {'pos_uuids': pos_uuid_list, 'search_name': "", 'filter': {}}
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        return self._session.put(
            url,
            json=data,
            headers=header
        )

    def unassigned(self, token, pos_uuid_list=[]):
        url = 'api/v1/playlist/pos/un_match'
        data = pos_uuid_list
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        return self._session.put(
            url,
            data=json.dumps(data),
            headers=header
        )

    def query_show_detail(self, token, pos_uuid):
        url = 'api/v1/schedule/detail?pos_uuid=' + pos_uuid

        return self._session.get(
            url,
            headers={
                'X-Thunderstorm-Key': token}
        )


if __name__ == '__main__':
    import datetime
    from features.setup import producer_login
    from features.constants import PRODUCER2_URI, PRODUCER2_PORTS

    token = producer_login()
    url = PRODUCER2_URI + PRODUCER2_PORTS['pv-sv']
    # res = ShowClient(url).query_show(token, '老', start_time='11:50',states=['unassigned'])
    # print('*' * 100)
    # a = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%H:%M")
    # print(a)
    # res = ShowClient(url).query_show(token)
    # print('*' * 1000)
    # resp = ShowClient(url).assigned(token, playlist_uuid='2c5b153f-7d3a-4ec6-a961-1ef05f5bcce9',
    #                                 pos_uuid_list=["8af81ca8-5843-4a78-8255-ce894fcb7a16"])
    # print(resp.json())
    resp = ShowClient(url).query_show_detail(token, pos_uuid='72d15518-7d15-4d42-a43b-b8766af70cfb')
    print(resp.json())
