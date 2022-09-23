from features.steps.api.api_utils.requests_session import RequestsSession
from urllib import parse
import json
from urllib.parse import quote


class SiteClient:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)

    def query_all_sites_in_complex_service(self, token):
        return self._session.get(
            'api/v3/complex?page_size=20&page=1',
            params=None,
            headers={'X-Thunderstorm-Key': token}
        )

    def query_site(self, params, token, filter=''):
        # encode = quote('{"status":["unuse"]}')
        # filter = '&filter=' + encode
        if filter != '':
            encode = quote(filter)
            filter = '&filter=' + encode

        path = f'api/v1/sites?page_num=1&page_size=5000' + filter

        params = json.loads(params)
        return self._session.get(
            path,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )

    def query_site_order(self, order_by, token):
        order_by = quote(order_by)
        return self._session.get(
            'api/v1/sites?page_num=1&page_size=5000&order_by='+order_by,
            headers={'X-Thunderstorm-Key': token}
        )

    def query_all_complex_groups(self, token):
        return self._session.get(
            'api/v1/complex-groups',
            headers={'X-Thunderstorm-Key': token}
        )

    def query_complexes(self, token, group_uuid, params=None):
        return self._session.get(
            f'api/v1/complex-groups/{group_uuid}/complexes',
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )

    # 获取影院设备
    def query_device(self, token, complex_uuid, params=None):
        return self._session.get(
            f'api/v1/complex/{complex_uuid}/device?page_num=1&page_size=500',
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )

    # 获取影院设备的cpl
    def query_device_content(self, token, complex_uuid, device_uuid, params=None, order_by='', filter=''):
        url = f'api/v1/content/complex/{complex_uuid}/{device_uuid}?page_num=1&page_size=500'
        if order_by != '':
            order_by = quote(order_by)
            url = url + '&order_by=' + order_by
        if filter != '':
            filter = quote(filter)
            url = url + '&filter=' + filter
        return self._session.get(
            url,
            params=params,
            headers={'X-Thunderstorm-Key': token}
        )
