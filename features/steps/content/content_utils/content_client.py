import datetime
import json
import logging
import time
from features.steps.cpl.cpl_utils.segment_cpl import SegmentCpl
from features.steps.api.api_utils.requests_session import RequestsSession
from urllib.parse import quote

from tools.logger import GetLogger
log=GetLogger().get_logger()


class Content:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)
        self.b=SegmentCpl(base_url)
    def create_content(self, token, content_title_text: str):

        '''创建content'''
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        log.info('请求header为{}'.format(header))
        data = {
            'content_title_text': content_title_text,
            'duration_numerator': 7200
        }

        return self._session.post(
            'api/v1/contents/save/placeholder',
            json=data,
            headers=header
        )

    def edit_content_attr_client(self,token,cpl_uuid:str,data):
        '''通过cpl_uuids编辑content'''
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        log.info('请求header为{}'.format(header))


        return self._session.put(
            'api/v1/contents/update/placeholder/patch/' + cpl_uuid,
            json=data,
            headers=header
        )

    def edit_content_offset(self, token, cpl_uuid, time: int,
                            modify_types='rolling_credit' or 'credit_offset' or 'hard_lock_offset' or 'screenwriter_credit_offset'):
        '''
        前提duration不为0
        通过cpl_uuids编辑content的offset
        '''
        a = self.b.get_cpl_detail(cpl_uuid=cpl_uuid, token=token)
        c = a.json().get('data').get('duration')
        if c == 0:
            return '请先设置duration的时间长度'
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        log.info('请求header为{}'.format(header))
        cpl_uuids = []
        cpl_uuids.append(cpl_uuid)
        modify_type = []
        modify_type.append(modify_types)
        data = {
            'cpl_uuids': cpl_uuids,
            modify_types: time,
            'modify_type': modify_type
        }

        return self._session.put(
            'api/v1/contents/update/placeholder/metas',
            json=data,
            headers=header
        )

    def query_content(self,token, params=None, filter='', order_by='', search_title=''):
        '''通过title查询content'''
        url = 'api/v1/content?page_size=10&page_num=1'
        if order_by != '':
            order_by = quote(order_by)
            url += '&order_by=' + order_by
        if filter != '':
            filter = quote(filter)
            url += '&filter=' + filter
        if search_title != '':
            search_title = quote(search_title)
            url += '&search_title=' + search_title
        return self._session.get(
            url,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )

    # def get_content_by_filter_complex_uuids(self, token, complex_uuids: str='' or '999f7f2f-ff24-4e37-bc0f-8d1aa9596970'):
    #     '''通过complex_uuids筛选content'''
    #     '''这里默认账号为Asta.Fan@artsalliancemedia.com上content的uuid'''
    #     encode = quote(
    #         'order_by={"added":"desc"}&filter={"complex_uuids":["ebf9ae95-bba2-41e2-b686-c530383fb8c2"]}' + complex_uuids,
    #         'utf-8')
    #
    #     return self._session.get(
    #         'api/v1/content',
    #         params='page_num=1&page_size=10000&' + encode,
    #         headers={'X-Thunderstorm-Key': token}
    #     )

    def query_all_content(self, token, params=None,
                      filter='{"content_types":["feature","trailer","other","rating","advertisement"]}', order_by='',num=''):
        '''查询10000条的content'''
        url = f'api/v1/content?page_size=10000&page_num={num}'
        if order_by != '':
            order_by = quote(order_by)
            url += '&order_by=' + order_by
        if filter != '':
            filter = quote(filter)
            url += '&filter=' + filter
        return self._session.get(
            url,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )


if __name__ == '__main__':
    from features.setup import producer_login
    from features.constants import PRODUCER2_URI, PRODUCER2_PORTS

    # token = producer_login()
    url = PRODUCER2_URI + PRODUCER2_PORTS['pv-sv']
    # a = Content(url).create_content(token, 'aaasqqsss rq')
    # b=Content(url).query_content_by_str(token,params='aaasqqsss q')
    # b=Content(url).get_content_by_filter_complex_uuids(token,'ebf9ae95-bba2-41e2-b686-c530383fb8c2')
    # c=Content(url).edit_content_attr_client(token=token,cpl_uuid='f64046cf-1004-4a7c-b7b7-4603dc79b0ed',resolution='2K')
    # d=Content(url).edit_content_offset(token=token,cpl_uuid='3603db26-6e27-4479-980f-53fcd19e2853' ,time=2000,modify_types= 'hard_lock_offset')
    # a=Content(url).edit_content_attr_client(token,cpl_uuid='a7e85292-aaed-4def-8057-bcade39db08b',language='ed')
    # print(a.json())
    print(url)