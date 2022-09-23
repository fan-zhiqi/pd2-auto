import json

from features.steps.site.site_util.site_client import SiteClient
from urllib.parse import quote
from random import choice


def query_all_sites_in_complex_service(context):
    site_client = SiteClient(context.site_url)
    res = site_client.query_all_sites_in_complex_service(context.token)
    response = json.loads(res.text)
    context.all_site_list = response['data']


def query_site_accurately(context):
    site = context.all_site_list[0]
    site_client = SiteClient(context.content_url)
    params = '{"search_name": "' + site['name'] + '"}'
    res = site_client.query_site(params, context.token)
    response = json.loads(res.text)
    site_list = response['data']
    for item in site_list:
        assert item['name'] == site['name'], f"精确搜索site名称错误,{item['name']}, {site['name']}"


def query_site_vaguely(context):
    site = context.all_site_list[0]
    site_client = SiteClient(context.content_url)
    search_name = site['name'][:2]
    params = '{"search_name": "' + search_name + '"}'
    res = site_client.query_site(params, context.token)
    response = json.loads(res.text)
    site_list = response['data']
    for item in site_list:
        assert site['name'].find(search_name) != -1, f"模糊搜索site名称错误,{site['name']}不包含{search_name}"


def query_site_not_exist(context):
    site = context.all_site_list[0]
    site_client = SiteClient(context.content_url)
    search_name = 'iam not exist haha'
    params = '{"search_name": "' + search_name + '"}'
    res = site_client.query_site(params, context.token)
    response = json.loads(res.text)
    site_list = response['data']
    assert len(site_list) == 0,  f"搜索不存在的site名称，返回了结果{search_name}"


def query_site_order_by_name(context):
    site_client = SiteClient(context.content_url)
    encode = '{"name": "asc"}'
    res = site_client.query_site_order(encode, context.token)
    res_asc = json.loads(res.text)
    site_asc = res_asc['data']
    encode = '{"name": "desc"}'
    res = site_client.query_site_order(encode, context.token)
    res_desc = json.loads(res.text)
    site_desc = res_desc['data']
    site_desc = reversed(site_desc)
    for i, res_d in enumerate(site_desc):
        assert res_d['name'] == site_asc[i]['name'], f'影院按名字的升降序排序不一样'


def query_site_order_by_status(context):
    site_client = SiteClient(context.content_url)
    encode = '{"status": "asc"}'
    res = site_client.query_site_order(encode, context.token)
    res_asc = json.loads(res.text)
    status_asc = res_asc['data']
    encode = '{"status": "desc"}'
    res = site_client.query_site_order(encode, context.token)
    res_desc = json.loads(res.text)
    status_desc = res_desc['data']
    status_desc = reversed(status_desc)
    for i, res_d in enumerate(status_desc):
        assert res_d['issue_level'] == status_asc[i]['issue_level'], f'影院按状态的升降序排序不一样'


def query_site_filter_by_city(context):
    site_client = SiteClient(context.content_url)
    res = site_client.query_site('{}', context.token)
    res_all = json.loads(res.text)['data']
    if len(res_all) == 0:
        return

    cur_country = choice(res_all)['address_country']
    params = '{"countries":["'+cur_country+'"]}'
    res = site_client.query_site('{}', context.token, filter=params)
    res_exist = json.loads(res.text)['data']
    for item in res_exist:
        assert item['address_country'].lower() == cur_country.lower(), f'按国家城市过滤结果不符合预期:参数:{params}'
        if item['address_country'] == cur_country:
            print("country: %s",item['address_country'])
    params = '{"countries":["DNEe"]}'
    res = site_client.query_site('{}', context.token, filter=params)
    res_dne = json.loads(res.text)['data']
    assert len(res_dne) == 0, f'搜索不存在的记录返回有结果,参数:{params}'

    cur_country_city = choice(res_all)
    params = '{"countries": ["'+cur_country_city['address_country']+'"], "cities": ["'+cur_country_city['address_city']+'"]}'
    res_exist = json.loads(res.text)['data']
    for item in res_exist:
        assert item['address_country'] == cur_country_city['address_country']\
            and item['address_city'] == cur_country_city['address_city'],\
            f'按国家城市过滤结果不符合预期:参数:{params}'

    params = '{"countries":["DNEe"], "cities": ["DNEe"]}'
    res = site_client.query_site('{}', context.token, filter=params)
    res_dne = json.loads(res.text)['data']
    assert len(res_dne) == 0, f'搜索不存在的记录返回有结果,参数:{params}'


def query_site_filter_by_organization(context):
    site_client = SiteClient(context.user_url)

    res = site_client.query_all_complex_groups(context.token)
    res_all_group = json.loads(res.text)['data']
    group_uuid = res_all_group[0]['uuid']

    res = site_client.query_complexes(context.token, group_uuid)
    res_complexes = json.loads(res.text)['data']

    site_client = SiteClient(context.content_url)
    # params = '{"site_groups":["'+group_uuid+'"]}'
    params = '{"site_groups":["241234"]}'
    res = site_client.query_site('{}', context.token, filter=params)
    res_site = json.loads(res.text)['data']

    for site in res_site:
        assert site

    print()


def query_site_filter_by_device(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_name = res_devices[0]['device_name']

    # 精确搜索
    res = site_client.query_device(context.token, complex_uuid, params={'search_title': device_name})
    res_accurate = json.loads(res.text)['data']
    for acc in res_accurate:
        assert acc['device_name'] == device_name, f'精确搜索设备的名称不一致, complex_uuid:{complex_uuid}, device_name:{device_name}'

    # 模糊搜索
    p = device_name[:2]
    res = site_client.query_device(context.token, complex_uuid, params={'search_title': p})
    res_vague = json.loads(res.text)['data']
    for vague in res_vague:
        assert vague['device_name'].find(p) != -1, f'模糊搜索设备的名称不一致, complex_uuid:{complex_uuid}, device_name:{device_name}'


def query_device_content(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']
    title = res_all_content[0]['title']
    print()
    # # 精确搜索
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, params={'search_title': title})
    res_accurate = json.loads(res.text)['data']
    for acc in res_accurate:
        assert acc['title'] == title, f'精确搜索设备的content名称不一致, complex_uuid:{complex_uuid}, title:{title}'

    # 模糊搜索
    title = title[:2]
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, params={'search_title': title})
    res_vague = json.loads(res.text)['data']
    for vague in res_vague:
        assert vague['title'].find(title) != -1 \
               or vague['content_title_text'].find(title) != -1, f'模糊搜索设备的content名称不一致, complex_uuid:{complex_uuid}, title:{title}'


def query_device_content_order_1(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    # 按title升序
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"title": "asc"}')
    res_title_asc = json.loads(res.text)['data']
    # 按title降序
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"title": "desc"}')
    res_title_desc = json.loads(res.text)['data']
    res_title_desc = reversed(res_title_desc)
    for i, title_d in enumerate(res_title_desc):
        assert res_title_asc[i]['title'] == title_d['title'], f'device_content按title排序不正确, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'


    # 按kdm升序
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"kdm_count":"asc"}')
    res_kdm_asc = json.loads(res.text)['data']
    # 按kdm降序
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"kdm_count":"desc"}')
    res_kdm_desc = json.loads(res.text)['data']
    res_kdm_desc = reversed(res_kdm_desc)
    for i, kdm_d in enumerate(res_kdm_desc):
        assert res_kdm_asc[i]['kdm_count'] == kdm_d['kdm_count'], f'device_content按kdm排序不正确, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'


def query_device_content_order_2(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    # 按asc升序
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"added":"asc"}')
    res_asc = json.loads(res.text)['data']
    # 按desc降序
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"added":"desc"}')
    res_desc = json.loads(res.text)['data']
    res_desc = reversed(res_desc)
    for i, add_d in enumerate(res_desc):
        assert res_asc[i]['uuid'] == add_d['uuid'], f'device_content按added排序不正确, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    # # 按cpl_size升序
    # res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"cpl_size":"asc"}')
    # res_asc = json.loads(res.text)['data']
    # # 按cpl_size降序 todo 有bug
    # res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"cpl_size":"desc"}')
    # res_desc = json.loads(res.text)['data']
    # res_desc = reversed(res_desc)
    # for i, res_d in enumerate(res_desc):
    #     assert res_asc[i]['uuid'] == res_d['uuid'], f'device_content按cpl_size排序不正确, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'


    # 按status升序
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"status":"asc"}')
    res_asc = json.loads(res.text)['data']
    # 按status降序
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, order_by='{"status":"desc"}')
    res_desc = json.loads(res.text)['data']
    res_desc = reversed(res_desc)
    for i, res_d in enumerate(res_desc):
        assert res_asc[i]['status'] == res_d['status'], f'device_content按status排序不正确, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'


def query_device_content_filter_category(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']
    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content

    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"content_types":["feature"]}')
    res_fea = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"content_types":["advertisement"]}')
    res_adv = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"content_types":["feature","advertisement"]}')
    res_fea_adv = json.loads(res.text)['data']

    def check(res, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            content = memo[item['uuid']]
            assert item['content_kind'] == content['content_kind'], f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'


    check(res_fea, '{"content_types":["feature"]}')
    check(res_adv, '{"content_types":["advertisement"]}')
    check(res_fea_adv, '{"content_types":["feature","advertisement"]}')


def query_device_content_filter_status(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content

    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"status":["inuse"]}')
    res_inuse = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"status":["unuse"]}')
    res_unuse = json.loads(res.text)['data']

    def check(res, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            content = memo[item['uuid']]
            assert item['status'] == content['status'], f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_inuse, '{"status":["inuse"]}')
    check(res_unuse, '{"status":["unuse"]}')


def query_device_content_filter_added(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content

    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"begin_date":1567267200000}')
    res_be = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"end_date":1568908799999}')
    res_end = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"begin_date":1568044800000,"end_date":1568908799999}')
    res_be_end = json.loads(res.text)['data']

    def check(res, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            content = memo[item['uuid']]
            assert item['status'] == content['status'], f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_be, '{"begin_date":1567267200000}')
    check(res_end, '{"end_date":1568908799999}')
    check(res_be_end, '{"begin_date":1568044800000,"end_date":1568908799999}')


def query_device_content_filter_dimension(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content

    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"playback_modes":["2d"]}')
    res_2d = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"playback_modes":["3d"]}')
    res_3d = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"playback_modes":["2d", "3d"]}')
    res_2d_3d = json.loads(res.text)['data']

    def check(res, formats, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            count = 0
            for res_format in item['format']:
                for format in formats:
                    if res_format == format:
                        count += 1
            assert count > 0, f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_2d, ["2D"],'{"playback_modes":["2d"]}')
    check(res_3d, ["3D"], '{"playback_modes":["3d"]}')
    check(res_2d_3d, ["2D", "3D"], '{"playback_modes":["2d", "3d"]}')


def query_device_content_filter_experience(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content


    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"experiences":["DBOX"]}')
    res_dbox = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"experiences":["IMAX"]}')
    res_imax = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"experiences":["DBOX","IMAX"]}')
    res_dbox_imax = json.loads(res.text)['data']

    def check(res, formats, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            count = 0
            for res_format in item['format']:
                for format in formats:
                    if res_format == format:
                        count += 1
            assert count > 0, f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_dbox, ["DBOX"],'{"experiences":["DBOX"]}')
    check(res_imax, ["IMAX"], '{"experiences":["IMAX"]}')
    check(res_dbox_imax, ["DBOX","IMAX"], '"experiences":["DBOX","IMAX"]}')


def query_device_content_filter_aspect_ratio(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content


    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"aspect_ratios":["Flat"]}')
    res_flat = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"aspect_ratios":["scope"]}')
    res_scope = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"aspect_ratios":["Flat","scope"]}')
    res_flat_scope = json.loads(res.text)['data']

    def check(res, formats, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            count = 0
            for res_format in item['format']:
                for format in formats:
                    if res_format == format:
                        count += 1
            assert count > 0, f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_flat, ["Flat"],'{"aspect_ratios":["Flat"]}')
    check(res_scope, ["scope"], '{"aspect_ratios":["scope"]}')
    check(res_flat_scope, ["Flat","scope"], '{"aspect_ratios":["Flat","scope"]}')


def query_device_content_filter_audio_format(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content


    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"audio_formats":["5.1"]}')
    res_51 = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"audio_formats":["7.1"]}')
    res_71 = json.loads(res.text)['data']

    def check(res, formats, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            count = 0
            for res_format in item['format']:
                for format in formats:
                    if res_format == format:
                        count += 1
            assert count > 0, f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_51, ["5.1"],'{"audio_formats":["5.1"]}')
    check(res_71, ["7.1"], '{"audio_formats":["7.1"]}')


def query_device_content_filter_audio_language(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content


    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"audio_langs":["en"]}')
    res_en = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"audio_langs":["zh"]}')
    res_zh = json.loads(res.text)['data']

    def check(res, lang, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            assert item['language'] == lang, f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_en, 'en','{"audio_langs":["en"]}')
    check(res_zh, "zh", '{"audio_langs":["zh"]}')


def query_device_content_filter_subtitle_langs(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content


    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"subtitle_langs":["en"]}')
    res_en = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"subtitle_langs":["zh"]}')
    res_zh = json.loads(res.text)['data']

    def check(res, lang, name):
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            assert item['subtitles'] == lang, f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_en, 'en','{"subtitle_langs":["en"]}')
    check(res_zh, "zh", '{"subtitle_langs":["zh"]}')


def query_device_content_filter_rating(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    memo = {}
    for content in res_all_content:
        memo[content['uuid']] = content


    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"ratings":[{"territoryName":"UK","value":"PG"}]}')
    res_1 = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"ratings":[{"territoryName":"UK","value":"PG"},{"territoryName":"UK","value":"12A"}]}')
    res_2 = json.loads(res.text)['data']

    def check(res, rs, name):
        # <class 'list'>: [{'rating': 'PG', 'territory': 'UK'}]
        for item in res:
            assert item['uuid'] in memo, f'按filter:{name}过滤结果不一致, 数据不存在, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'
            rating = item['rating']
            count = 0
            for rate in rating:
                for r in rs:
                    if rate['rating'] == r['value'] and rate['territory'] == r['territoryName']:
                        count += 1
            assert count > 0, f'按filter:{name}过滤结果不一致, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}'

    check(res_1, [{"territoryName":"UK","value":"PG"}],'{"ratings":[{"territoryName":"UK","value":"PG"}]}')
    check(res_2, [{"territoryName":"UK","value":"PG"},{"territoryName":"UK","value":"12A"}], '{"ratings":[{"territoryName":"UK","value":"PG"},{"territoryName":"UK","value":"12A"}]}')


def query_device_content_filter_site(context):
    all_site_list = context.all_site_list
    complex_uuid = all_site_list[0]['uuid']
    site_client = SiteClient(context.content_url)
    res = site_client.query_device(context.token, complex_uuid)
    res_devices = json.loads(res.text)['data']
    device_uuid = res_devices[0]['device_uuid']

    res_all_content = site_client.query_device_content(context.token, complex_uuid, device_uuid)
    res_all_content = json.loads(res_all_content.text)['data']

    p_session = context.producer_view_session
    res = p_session.execute(f'''
        SELECT DISTINCT(cp.uuid),cp.content_name, cd.`name` 
        FROM cpl_locations_mapping clm,cpl_data cp, complex_data cd 
        WHERE clm.cpl_uuid = cp.uuid 
        AND clm.complex_uuid = cd.uuid AND 
        clm.complex_uuid = '{complex_uuid}' 
        AND clm.device_uuid = '{device_uuid}';
        ''')


    rm = res.fetchone()
    complex_name = rm[2]

    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"complex_names":["'+complex_name+'"]}')
    res_e = json.loads(res.text)['data']
    res = site_client.query_device_content(context.token, complex_uuid, device_uuid, filter='{"complex_names":["a e a 3 4 1"]}')
    res_dne = json.loads(res.text)['data']

    assert len(res_e) > 0, f'按存在的影院查询content, 返回为空, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}, complex_name:{complex_name}'
    assert len(res_dne) == 0, f'按不存在的影院查询content, 返回有数据, complex_uuid:{complex_uuid}, device_uuid:{device_uuid}, complex_name:{"a e a 3 4 1"}'