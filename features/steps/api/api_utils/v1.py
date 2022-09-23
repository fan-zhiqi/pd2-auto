import json

from features.constants import PRODUCER2, PRODUCER2_URI, PRODUCER2_PORTS
from features.steps.api.api_utils.requests_session import RequestsSession

class V1:

    def __init__(self, base_url):
        self._session = RequestsSession(base_url)

    def login(self, arguments: dict) -> dict:
        """ The User can login to Frontend-UI
        Example for data:
        {
           "email": "testing@test.com",
           "password": "pazzw0rd"
        }
        """

        res = self._session.post(
            'api/v1/auth/login',
            json=arguments,
            headers={'Content-Type': 'application/json;charset=utf-8;charset=utf-8'}

        )
        tk = res.json()["token"]
        self._session.headers = {"X-Thunderstorm-Key": tk, "User-Agent": "AAM-debug.dev.io"}
        return self._session.headers


    def logout(self):
        """ The User can logout of Frontend-UI"""

        return self._session.post('api/v1/logout')


    def create_site_alias_and_assign_device(self, arguments: dict) -> dict:
        """ Creates a Site Alias and assigns a device to it
        Example for data:
        {
           "siteName": "site_alias_name_1",
           "deviceID": 1
        }
        """

        return self._session.post('api/v1/assign-device', data=arguments)
if __name__ == '__main__':

    data = {
        "username": PRODUCER2["username"],
        "password": PRODUCER2["password"]
    }

    login_url = PRODUCER2_URI + PRODUCER2_PORTS['producer2']
    p = V1(login_url)
    s = p.login(data)
    print(s['X-Thunderstorm-Key'])