# encoding: utf-8
import os
from datetime import datetime
from tools import sendEmail
project_path = os.path.dirname(os.path.abspath(__file__))
print(project_path)


def run():
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    os.system('behave -f allure_behave.formatter:AllureFormatter -o ./reports/%s' % now)
    # os.system('allure generate ./reports/{} -o ./reports/allure_html --clean'.format(now))
    os.system('allure generate ./reports/{0} -o /usr/share/nginx/html/{0} --clean'.format(now))
    # os.system('behave --tags=@create_title_segment_add_auto_playlist -f allure_behave.formatter:AllureFormatter -o ./reports/%s' % now)
    # sendEmail.mail('http://172.31.105.34/index.html')
    # os.system('allure serve {0} -p 9998 ./reports/%s' %now)

if __name__ == '__main__':
    n1 = datetime.now()
    import jsonpath
    import time
    from features.steps.playlist.playlist_utils.playlist_client import Playlist
    from features.setup import producer_login
    from features.constants import PRODUCER2_URI, PRODUCER2_PORTS
    token = producer_login()
    url2 = PRODUCER2_URI + PRODUCER2_PORTS['playlist']
    playlist_client = Playlist(url2)
    res = playlist_client.query_playlist_by_title(token)
    uuid = jsonpath.jsonpath(res.json(), '$..pplUuid')
    if uuid:
        for i in uuid:
            playlist_client.delete_playlist(token, i)
        time.sleep(10)
    run()
    n2 = datetime.now()
    n3 = (n2 - n1).seconds
    print(f'运行总时长{n3}s')
