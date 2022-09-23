from features.steps.api.api_utils.requests_session import RequestsSession
from urllib import parse
import json
from urllib.parse import quote


class SegmentClient:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)

    def create_segment(self, token, data):
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        return self._session.post(
            'api/v1/playlist/segment',
            json=data,
            headers=header
        )

    def query_segment_by_title(self, token, title=''):
        '''1.7工单有改动，先types为全选，后期修改'''
        url = 'api/v1/playlist/segment'
        params = {}
        a = {'title': title, 'types': []}
        params['search'] = json.dumps(a)
        # search: {"title": "Intermission",
        #          "types": ["api_segment", "playlist_segment", "title_segment", "rating_segment", "base_segment"]}
        return self._session.get(
            url,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )

    def query_segment(self, token, params=None, search='', filter='', order_by=''):
        url = 'api/v1/playlist/segment?page_size=5000&page_num=1'
        if order_by != '':
            order_by = quote(order_by)
            url += '&order_by=' + order_by
        if search != '':
            search = quote(search)
            url += '&search=' + search
        if filter != '':
            filter = quote(filter)
            url += '&filter=' + filter
        return self._session.get(
            url,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )

    def query_segment_split_detail(self, token, content_association_uuid, title_uuid=''):
        '''1.7工单有改动，先types为全选，后期修改'''
        url = 'api/v1/playlist/segment_split'
        params = {
            'content_association_uuid': content_association_uuid,
            'title_uuid': title_uuid
        }
        return self._session.get(
            url,
            params=params,
            headers={
                'Content-Type': 'application/json;charset=utf-8',
                'X-Thunderstorm-Key': token
            })

    def add_draft_to_title_segment(self, token, data):
        '''data=playlist_version_uuid,playlist_uuid,content_list:[],show_attribute_grounps:[]'''
        return self._session.put(
            'api/v1/playlist/segment_split/update_content',
            json=data,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def publish_title_segment(self, token, content_association_uuid, action_tag_uuid, title_uuid=''):
        '''data=playlist_version_uuid,playlist_uuid,content_list:[],show_attribute_grounps:[]'''
        data = {"publish_later": False, "week_split": False, "action_tag_uuid": action_tag_uuid}
        return self._session.put(
            f'api/v1/playlist/segment_split/publish?title_uuid={title_uuid}&content_association_uuid={content_association_uuid}',
            json=data,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )


    def query_segment_manage_shows(self,token,split_uuid,content_association_uuid,title_uuid):
        pa={ 'split_id': split_uuid,
        'search_name':'',
        'page_num': 1,
        'page_size': 100,
        'filters': {"show_attribute_search_type": 1},
        'content_association_uuid': content_association_uuid,
        'title_uuid': title_uuid
        }
        return self._session.get(
            'api/v1/schedule/split/manage/show',
            params=pa,
            headers={
                'Content-Type': 'application/json;charset=utf-8',
                'X-Thunderstorm-Key': token
            })