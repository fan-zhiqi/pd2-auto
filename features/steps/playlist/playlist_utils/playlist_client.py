import jsonpath

from features.steps.api.api_utils.requests_session import RequestsSession
from urllib import parse
import json
from urllib.parse import quote


class Playlist:
    '''
    方法：
    create_static_playlist:创建静态playlist
    get_playlist_version_uuid：获取playlist_version_uuid
    add_draft_to_static_playlist：保存草稿
    '''

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)

    def create_static_playlist(self, token, title):
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        data = {
            "automatically_apply": 'false',
            "title": title
        }
        return self._session.post(
            'api/v1/playlist/ppl/standard',
            json=data,
            headers=header
        )

    def query_playlist_version_uuid_and_other_detail(self, token, playlist_uuid):

        header = {'X-Thunderstorm-Key': token}
        return self._session.get(
            'api/v1/playlist/ppl/' + playlist_uuid,
            params='versions=draft&release',
            headers=header
        )

    def query_content_in_library(self, token, library_type: str = None, search_title: str = None,
                                 segment_type: str = None,device_type='',device_model=''):
        '''page_num: 1
        page_size: 25
        filter: {"library_type": "cpl", "search_title": "169455",
                 "content_filter": {"segment_type": "api_segment,base_segment,title_segment"}}
        filter: {"library_type":"automation","content_filter":{"device_type":"emulator","device_model":"T1000"}}
                 '''

        params = {
            "page_num": 1,
            "page_size": 25
        }
        filter_dict = {"library_type": library_type, "content_filter": {}}
        if segment_type:
            filter_dict["content_filter"]["segment_type"] = segment_type
        if device_type:
            filter_dict["content_filter"]['device_type']=device_type
        if device_model:
            filter_dict["content_filter"]['device_model']=device_model
        if search_title:
            filter_dict["search_title"] = search_title

        _json = json.dumps(filter_dict)
        st = str(_json)
        params["filter"] = st
        return self._session.get(
            'api/v1/content/library',
            params=params,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def add_draft_to_playlist(self, token, data, playlist_version):
        '''data=playlist_version_uuid,playlist_uuid,content_list:[],show_attribute_grounps:[]'''
        return self._session.put(
            'api/v1/playlist/playlist_version/' + playlist_version,
            json=data,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def query_playlist_by_title(self, token, playlist_title=''):
        params = {
            "page_num": 1,
            "page_size": 1000,
        }
        a = {"title": playlist_title, "status": [], "types": [], "shows": [], "order_by_name": "name",
             "order_by_desc": True}
        params['search'] = json.dumps(a)
        return self._session.get(
            'api/v1/playlist/ppl',
            params=params,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def query_show_attribute(self, token):
        return self._session.get(
            'api/v3/show_attribute',
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def create_auto_playlist(self, token, attribute_name, playlist_title, attrbute=[]):
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        data = {
            "title": playlist_title,
            "show_attribute_groups": [{"name": attribute_name, "attributes": attrbute}],
            "automatically_apply": True
        }
        return self._session.post(
            'api/v1/playlist/ppl/automatic',
            json=data,
            headers=header
        )

    def publish(self, token, data, playlist_version):
        '''data=playlist_version_uuid,playlist_uuid,content_list:[],show_attribute_grounps:[]'''
        return self._session.put(
            'api/v1/playlist/playlist_version/' + playlist_version + '/publish',
            json=data,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def query_playlist_manage_shows(self, token, playlist_type, automatically_apply, playlist_uuid, show_attribute):
        '''
            playlist_type:DRAFT_MATCH|DRAFT_NOT_MATCH|RELEASE_MATCH|RELEASE_NOT_MATCH
         automatically_apply: bool,Flase为standard，True为auto
         show_attributes：[[],[]]
        '''
        # a = {}
        # params = {
        #     'playlist_type': playlist_type,
        #     'ppl_uuid': playlist_uuid,
        #     'automatically_apply': automatically_apply,
        #     'show_attributes': [],
        #     "page_num": 1,
        #     "page_size": 25,
        #     'filters': json.dumps(a)
        # }

        url = f'api/v1/schedule/playlist/manage/show?playlist_type={playlist_type}&ppl_uuid={playlist_uuid}&show_attributes={show_attribute}&automatically_apply={automatically_apply}&page_num=1&page_size=100'
        return self._session.get(
            url,
            # 'api/v1/schedule/playlist/manage/show',
            # params=params,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def query_process_queues(self, token, name='', sections=[], status=[]):
        '''
        name:playlist_title...
        sections:模块功能名称有"playlist","macro","segment","show","cpl","title","screen","pack","schedule
        status:"success","pending","failed","locked"
        {"name":null,"sections":["playlist","macro","segment","show","cpl","title","screen","pack","schedule"],"status":["success","pending","failed","locked"]}
        '''
        params = {
            "page_num": 1,
            "page_size": 25,
        }
        a = {'name': name, 'sections': sections, 'status': status}
        params['search'] = json.dumps(a)
        return self._session.get(
            'api/v1/assign_mission',
            params=params,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def delete_playlist(self, token, playlist_uuid):
        return self._session.delete(
            'api/v1/playlist/ppl/' + playlist_uuid,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )


if __name__ == '__main__':
    def dict_to_json_str(source: dict):
        if not source:
            return
        return json.dumps(source)


    from features.setup import producer_login
    from features.constants import PRODUCER2_URI, PRODUCER2_PORTS

    token = producer_login()
    # url = PRODUCER2_URI + PRODUCER2_PORTS['site']
    # playlist_client = Playlist(url)
    # a = playlist_client.query_show_attribute(token)
    # print(a.json().get('data')[0])
    url1 = PRODUCER2_URI + PRODUCER2_PORTS['playlist']
    url2 = PRODUCER2_URI + PRODUCER2_PORTS['pv-sv']
    playlist_client = Playlist(url1)
    playlist_client2 = Playlist(url2)
    res = playlist_client.query_process_queues(token)
    # print(res)
    # res = playlist_client2.query_playlist_manage_shows(token,playlist_type='RELEASE_MATCH', automatically_apply=False,
    #                                                    playlist_uuid='20803c21-b86e-42a2-afa2-fe2a29d31fb5')

    print(res.json())
    # a=playlist_client.create_static_playlist(token, 'aaaa')
    # url2 = PRODUCER2_URI + PRODUCER2_PORTS['pv-sv']
    # a = Playlist(url2)
    # # f=a.query_playlist_by_title(token,'playlist_edit_content_titie4318243686')
    # b = a.query_content_in_library(token, library_type='cpl', search_title='bb364f3e-d2d2-466d-8205-c061aae17b4c')
    # c = jsonpath.jsonpath(b.json(), '$...data[?(@.content_id=="bb364f3e-d2d2-466d-8205-c061aae17b4c")]')
    # dict_to_json_str(c[0]['extension'])
    # e = {'playlist_uuid': '16e63689-3d55-4172-bac0-fb530b4d1c94',
    #      'content_list': c}
    # # print(jsonpath.jsonpath(b.json(),'$...data[?(@.content_id=="bb364f3e-d2d2-466d-8205-c061aae17b4c")]'))
    # f = Playlist(url).add_draft_to_static_playlist(token, data=e,
    #                                                playlist_version='5f896547-6de3-481e-99ac-fe29c62c4c14')

    # # print(f.json)
    # print(f.headers)
    # d = c[0]['extension']
    # print(f.json())
    # d = str(json.dumps(d))
    # print(type(d))
    # print(version.json())
    # a = jsonpath.jsonpath(version.json(), '$...data.versions[?(@.status=="draft")]')
    # print(a)
    # print(a[0]['playlist_version_uuid'])
