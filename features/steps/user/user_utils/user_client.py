#!/usr/bin/python
# -*-coding:utf-8 -*-
from features.steps.api.api_utils.requests_session import RequestsSession
from features import constants

class UserClient:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)
    def change_org(self,token):
        '''创建title'''
        header = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Thunderstorm-Key': token
        }
        organization_uuid=constants.organization_uuid
        data = {
          'organization_uuid':organization_uuid
        }
        return self._session.post(
            'api/v1/changeOrganization',
            json=data,
            headers=header
        )