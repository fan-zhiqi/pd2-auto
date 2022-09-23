import logging

import allure
import requests
from retrying import retry

from tools.logger import GetLogger

log = GetLogger().get_logger()

from typing import Dict, List, Union, Any

from requests import Response

JSONType = Union[
    Dict[str, Any],
    List[Any]
]


class RequestsSession(object):

    def __init__(self, base_url: str):
        self._base_url = base_url
        self._session = requests.Session()

    def get(
            self,
            endpoint: str,
            params: dict = None,
            headers: dict = None,
            **kwargs
    ) -> JSONType:
        headers = headers or {}

        return self._request(
            method='GET',
            url=self._url(endpoint),
            params=params,
            headers=headers,
            **kwargs
        )

    def post(
            self,
            endpoint: str,
            json: dict = None,
            data: dict = None,
            params: dict = None,
            files: dict = None,
            headers: dict = None
    ) -> JSONType:
        headers = headers or {}
        data = data or {}
        json = json or {}

        if headers:
            # headers = self._updated_headers(headers or {})
            headers = headers

        return self._request(
            method='POST',
            url=self._url(endpoint),
            json=json,
            data=data,
            params=params,
            headers=headers,
            files=files
        )

    def put(
            self,
            endpoint: str,
            data: dict = None,
            json: dict = None,
            params: dict = None,
            headers: dict = None
    ) -> JSONType:
        headers = headers or {}
        data = data or {}
        json = json or {}

        # if headers:
        # headers = self._updated_headers(headers or {})

        return self._request(
            'PUT',
            self._url(endpoint),
            data=data,
            json=json,
            params=params,
            headers=headers
        )

    def patch(
            self,
            endpoint: str,
            data: dict = None,
            json: dict = None,
            params: dict = None,
            headers: dict = None
    ) -> JSONType:
        headers = headers or {}
        data = data or {}
        json = json or {}

        # if headers:
        #     headers = self._updated_headers(headers or {})

        return self._request(
            'PATCH',
            self._url(endpoint),
            data=data,
            json=json,
            params=params,
            headers=headers
        )

    def delete(
            self,
            endpoint: str,
            data: dict = None,
            json: dict = None,
            params: dict = None,
            headers: dict = None
    ) -> JSONType:
        headers = headers or {}
        data = data or {}
        json = json or {}

        # if headers:
        #     headers = self._updated_headers(headers or {})

        return self._request(
            'DELETE',
            self._url(endpoint),
            data=data,
            json=json,
            params=params,
            headers=headers
        )

    @retry(stop_max_attempt_number=1, wait_fixed=2000)
    def _request(self, method, url, **kwargs) -> Response:
        try:
            resp = self._session.request(method=method, url=url, timeout=5, **kwargs)
            log.info('请求的url为{}'.format(resp.request.url))
            print(f'请求方式{resp.request.method}:url:{resp.request.url}')
            print(f'请求参数:{resp.request.body}')

            with allure.step(f'log{url}'):
                allure.attach(name='请求方式:', body=resp.request.method)
                allure.attach(name='请求url:', body=resp.request.url)
                allure.attach(name='请求参数:', body=str(resp.request.body))
                allure.attach(name='响应数据:', body=resp.content or '请求响应为空')
            if len(resp.content):
                print(resp.content)
                logging.info(resp.content)

            else:
                print('请求响应为空')
                logging.info('请求响应为空')
        except TimeoutError:
            resp = 'TimeoutError'
            with allure.step(f'log{url}'):
                allure.attach(name='请求方式:', body=method)
                allure.attach(name='请求url:', body=url)
                allure.attach(name='请求参数:', body=str(kwargs))
                allure.attach(name='响应数据:', body='接口响应时间超过5s')
        except(Exception, BaseException) as e:
            resp = 'otherException'
            with allure.step(f'log{url}'):
                allure.attach(name='请求方式:', body=method)
                allure.attach(name='请求url:', body=url)
                allure.attach(name='请求参数:', body=str(kwargs))
                allure.attach(name='响应数据:', body=repr(e))
        return resp

        # print(f'请求结果{resp.json()}')
        # print('请求头：',resp.request.headers)
        # print_content = ''
        # if len(resp.content) > 10000:
        #     print_content = resp.content[:10000]
        # else:
        #     print_content = resp.content
        # if resp.status_code == 500:
        #     print(f'返回错误:{print_content}')
        #     log.info(f'返回错误:{print_content}')
        # resp.raise_for_status()
        # # print(f'返回结果:{print_content}')
        # log.info(f'返回结果:{print_content}')

    def _updated_headers(self, headers) -> dict:
        current_headers = self._session.headers.copy()
        return current_headers.update(headers)

    def _url(self, endpoint) -> str:
        return f'{self._base_url}/{endpoint}'


if __name__ == '__main__':
    json = {'username': 'k8stest', 'password': 'test2018?'}
    header = {'Content - Type': 'application / json;charset = utf - 8', 'Env': 'test',
              'Cookie': 'locale=en-US;_csrf=w3Lr3AoaLzda2bA36mPnb2DU;XSRF-TOKEN=B0JlMAPF--e3E4fWPTrGhs5k0wv3N1Pscqpc; logged=1;token_id=',
              'X-XSRF-TOKEN': 'B0JlMAPF--e3E4fWPTrGhs5k0wv3N1Pscqpc'}
    RequestsSession("http://k8s-test-1.aamcn.com.cn:30493").post(endpoint='aam/user/api/v1/auth/login', json=json,
                                                                 headers=header)
