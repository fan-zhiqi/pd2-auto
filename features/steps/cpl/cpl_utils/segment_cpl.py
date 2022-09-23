from features.steps.api.api_utils.requests_session import RequestsSession
from urllib.parse import quote


class SegmentCpl:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)

    def update_cpl_segment(self, data: dict, token: str):
        return self._session.patch(
            'api/v1/cpl/metas',
            json=data,
            headers={'Content-Type': 'application/json;charset=utf-8', 'X-Thunderstorm-Key': token}
        )

    def get_cpl_detail(self, cpl_uuid, token):
        return self._session.get(
            f'api/v1/content/{cpl_uuid}'+'?cpl_uuid='+cpl_uuid,
            headers={'X-Thunderstorm-Key': token}
        )

    def delete_cpl(self, complex_uuid, cpl_uuid, device_uuids, token):
        return self._session.delete(
            f'api/v1/cpl/{cpl_uuid}',
            params='locations=[{"complex_uuid":"' + complex_uuid + '","on_devices":["' + device_uuids + '"]}]',
            headers={'X-Thunderstorm-Key': token}
        )

    def get_play_list(self,token: str, title: str):
        return self._session.get(
            'api/v1/playlist/ppl',
            params='page_num=1&page_size=50&search={"title":"'+title+'"}',
            headers={'X-Thunderstorm-Key': token}
        )

    def get_cpl_list(self, token):
        encode = quote('{"status":["unuse"],"content_types":["feature","advertisement","rating","trailer","other"]}')
        filter = '&filter=' + encode
        return self._session.get(
            'api/v1/content',
            params='page_num=1&page_size=100%s' % filter,
            headers={'X-Thunderstorm-Key': token}
        )

    def get_complex_device_uuid(self,token, cpl_uuid):
        return self._session.get(
            f'api/v1/content/{cpl_uuid}/usage',
            headers={'X-Thunderstorm-Key': token}
        )