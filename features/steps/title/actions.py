#!/usr/bin/python
#-*-coding:utf-8 -*-
import json
import logging
from urllib.parse import quote
import time, datetime

import jsonpath

from features.steps.title.title_utils.title_client import TitleClient
from features.steps.site.site_util.site_client import SiteClient
from features.steps.content.content_utils.content_client import Content

from tools.logger import GetLogger

log = GetLogger().get_logger()

import random


def create_title(context, name):
    context.name = name + str(random.randint(1300000000, 14000000000))
    title_client = TitleClient(context.title_url)
    log.info('请求参数为name:{}，source_id:{}'.format(context.name, context.source_id))
    res = title_client.create_title(context.token, context.name, context.source_id)
    context.resp = res.json()
    context.title_uuid = context.resp['data']
    return context.resp


def query_movies_id(context):
    search_text = chr(random.randint(97, 122))
    res = TitleClient(context.title_url).query_movies(context.token, search_text)
    context.resp = res.json()
    context.source_id = jsonpath.jsonpath(context.resp, '$..source_id')[0]
    return context.resp


def create_lack_name_title(context):
    name = ''
    source_id = 809107
    title_client = TitleClient(context.title_url)
    log.info('请求参数为name:{}，source_id:{}'.format(name, source_id))
    res = title_client.create_title(context.token, name, source_id)
    context.resp = res.json()
    return context.resp


def create_lack_source_id_title(context):
    random_name = str(random.randint(1300000000, 14000000000))
    source_id = ''
    title_client = TitleClient(context.title_url)
    log.info('请求参数为name:{}，source_id:{}'.format(random_name, source_id))
    res = title_client.create_title(context.token, random_name, source_id)
    context.resp = res.json()
    return context.resp


def create_repeat_title(context, name):
    title_client = TitleClient(context.title_url)
    res = title_client.query_title_by_str(token=context.token, search_text=name)
    name_list = jsonpath.jsonpath(res.json(), '$..name')
    if name in name_list:
        res2 = title_client.create_title(context.token, name, context.source_id)
    else:
        res = title_client.create_title(context.token, name, context.source_id)
        res2 = title_client.create_title(context.token, name, context.source_id)
    context.resp = res2.json()
    return context.resp


def query_title_by_str(context):
    title_client = TitleClient(context.title_url)
    res = title_client.query_title_by_str(token=context.token, search_text=context.name)
    context.resp = res.json()
    context.title_uuid_list = jsonpath.jsonpath(context.resp, '$..uuid')
    logging.info(context.title_uuid_list)
    return context.resp


def query_title(context):
    title_client = TitleClient(context.title_url)
    res = title_client.query_title(context.token)
    res_all = json.loads(res.text)['data']
    title = res_all[0]['name']

    search_text = title
    res = title_client.query_title(context.token, search_text=search_text)
    res_ = json.loads(res.text)['data']
    for item in res_:
        assert item['name'].find(title) != -1, f'查询title结果不正确, 参数:{search_text}'

    search_text = "ia m no t exis t!de"
    res = title_client.query_title(context.token, search_text=search_text)
    res_ = json.loads(res.text)['data']
    assert len(res_) == 0, f'查询不存在的title, 返回title有结果, 参数:{search_text}'


def query_title_by_asc_and_desc(context):
    title_client = TitleClient(context.title_url)
    # 升序
    encode = quote('{"name": "asc"}')
    params = '?page_num=1&page_size=5000&order_by=' + encode
    asc_res = title_client.query_title_by_str(params, context.token)
    asc_response = json.loads(asc_res.text)
    context.asc_title_list = asc_response['data']
    # 倒序
    encode = quote('{"name": "desc"}')
    params = '?page_num=1&page_size=5000&order_by=' + encode
    desc_res = title_client.query_title_by_str(params, context.token)
    desc_response = json.loads(desc_res.text)
    context.desc_title_list = desc_response['data']


def query_a_title_has_playlist(context):
    # query_title(context, "{}", False)
    title_client = TitleClient(context.title_url)
    res = title_client.query_title(context.token)
    res_all = json.loads(res.text)['data']
    context.title_list = res_all
    res = context.title_list
    assert res is not None and len(res) > 0, '找不到任何title列表'
    title_client = TitleClient(context.playlist_url)
    # 遍历直到有播放列表为止
    for title in res:
        title_uuid = title['uuid']
        params = f'?title_uuid={title_uuid}'
        response = json.loads(title_client.query_title_playlist(params, context.token).text)
        if response['code'] == 200 and 'data' in response and response['data'] is not None and len(
                response['data']) > 0:
            context.title = title
            context.title_playlists = response['data']
            return
    raise RuntimeError('找不到任何含有playlist的title')


def query_title_playlist_strictly(context):
    title_uuid = context.title['uuid']
    playlists = context.title_playlists
    title_client = TitleClient(context.playlist_url)
    for playlist in playlists:
        title = playlist['title']
        params = f'?title_uuid={title_uuid}&title={title}'
        response = json.loads(title_client.query_title_playlist(params, context.token).text)
        for data in response['data']:
            if data['title'] == title:
                return
        raise RuntimeError(f'精确搜索没找到此title_playlist, title:{title}, title_uuid:{title_uuid}')


def query_title_playlist_vaguely(context):
    title_uuid = context.title['uuid']
    playlists = context.title_playlists
    title_client = TitleClient(context.playlist_url)
    for playlist in playlists:
        title = playlist['title']
        if len(title) > 1:
            title = title[:len(title) - 1]
        params = f'?title_uuid={title_uuid}&title={title}'
        response = json.loads(title_client.query_title_playlist(params, context.token).text)
        for data in response['data']:
            if data['title'].find(title) != -1:
                return
        raise RuntimeError(f'模糊搜索没找到此title_playlist, title:{title}, title_uuid:{title_uuid}')


def query_title_playlist_not_exist(context):
    title_uuid = context.title['uuid']
    playlists = context.title_playlists
    title_client = TitleClient(context.playlist_url)
    for playlist in playlists:
        title = 'Im not existserdfadx'
        params = f'?title_uuid={title_uuid}&title={title}'
        response = json.loads(title_client.query_title_playlist(params, context.token).text)
        for data in response['data']:
            assert len(data) == 0, f'断言搜索没找到此title_playlist, 但返回不为空的列表，title:{title}, title_uuid:{title_uuid}'


def query_a_title_has_show(context):
    title_client = TitleClient(context.title_url)
    res = title_client.query_title(context.token)
    res_all = json.loads(res.text)['data']
    res = res_all
    assert res is not None and len(res) > 0, '找不到任何title列表'
    title_client = TitleClient(context.posuuid_url)
    # 遍历直到有show列表为止
    for title in res:
        title_uuid = title['uuid']
        params = '{"title_uuid":"' + title_uuid + '"}'
        response = json.loads(title_client.query_title_show(params, context.token).text)
        if response['code'] == 200 and 'data' in response and response['data'] is not None and len(
                response['data']) > 0:
            context.title = title
            context.title_shows = response['data']
            return
    raise RuntimeError('找不到任何含有show的title')


def query_title_shows_strictly(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    for show in shows:
        title_name = show['name']
        params = '{"title_uuid":"' + title_uuid + '"}'
        response = json.loads(title_client.query_title_show(params, context.token, search_name=title_name).text)
        res_data = response['data']
        for data in res_data:
            assert data['name'] == context.title[
                'name'], f'查询show的name:{data["name"]}与title_name:{context.title["name"]}不一致'


def query_title_shows_vaguely(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    for show in shows:
        title_name = show['name']
        if len(title_name) > 1:
            title_name = title_name[:len(title_name) - 1]
        params = '{"title_uuid":"' + title_uuid + '"}'
        response = json.loads(title_client.query_title_show(params, context.token, search_name=title_name).text)
        res_data = response['data']
        for data in res_data:
            assert data['name'].find(
                title_name) != -1, f'查询show的name:{data["name"]}不包含title_name:{context.title["name"]}'


def query_title_shows_not_exist(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    title_name = "I'm not exist in this system faioqwxc"
    params = '{"title_uuid":"' + title_uuid + '"}'
    response = json.loads(title_client.query_title_show(params, context.token, search_name=title_name).text)
    assert len(response['data']) == 0, '搜索一个理应不存在的show, 但返回不为空'


def query_title_shows_by_attribute_strictly(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.posuuid_url)
    for show in shows:
        attributes = show['pos_show_attributes']
        # attributes = quote(attributes)
        if attributes is None or len(attributes) == 0:
            continue
        attribute = attributes[0]
        params = '{"title_uuid":"' + title_uuid + '"}'
        response = json.loads(title_client.query_title_show(params, context.token, search_name=attribute).text)
        res_data = response['data']
        for data in res_data:
            count = 0
            for attr in data['pos_show_attributes']:
                if attr == attribute:
                    count += 1
                    break
            if count == 0:
                raise RuntimeError(
                    f'找不到有关attribute:{attribute}的show, title_uuid:{title_uuid}, data:{data["pos_show_attributes"]}')


def query_title_shows_by_attribute_not_exist(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    attribute = 'iDNEa'
    params = '{"title_uuid":"' + title_uuid + '"}'
    response = json.loads(title_client.query_title_show(params, context.token, search_name=attribute).text)
    res_data = response['data']
    assert len(res_data) == 0, f'用不存在的attribute:{attribute}搜索,返回数据有列表长度, title_uuid:{title_uuid}'


def query_title_shows_order_by_show_name(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    params = '{"title_uuid":"' + title_uuid + '"}'
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"title": "desc"}').text)
    res_desc = response['data']
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"title": "asc"}').text)
    res_asc = response['data']
    assert len(res_desc) == len(res_asc), f'升序与降序数目不一样, title_uuid:{title_uuid}'
    res_asc = reversed(res_asc)
    for i, item in enumerate(res_asc):
        assert res_desc[i]['name'] == item['name'], '升序与降序对比不一致'


def query_title_shows_order_by_start_time(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    params = '{"title_uuid":"' + title_uuid + '"}'
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"start_time": "desc"}').text)
    res_desc = response['data']
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"start_time": "asc"}').text)
    res_asc = response['data']
    assert len(res_desc) == len(res_asc), f'升序与降序数目不一样, title_uuid:{title_uuid}'
    res_asc = reversed(res_asc)
    for i, item in enumerate(res_asc):
        assert res_desc[i]['name'] == item['name'], '升序与降序对比不一致'


def query_title_shows_order_by_site(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    params = '{"title_uuid":"' + title_uuid + '"}'
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"site": "desc"}').text)
    res_desc = response['data']
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"site": "asc"}').text)
    res_asc = response['data']
    assert len(res_desc) == len(res_asc), f'升序与降序数目不一样, title_uuid:{title_uuid}'
    res_asc = reversed(res_asc)
    for i, item in enumerate(res_asc):
        assert res_desc[i]['name'] == item['name'], '升序与降序对比不一致'


def query_title_shows_order_by_screen(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    params = '{"title_uuid":"' + title_uuid + '"}'
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"screen": "desc"}').text)
    res_desc = response['data']
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"screen": "asc"}').text)
    res_asc = response['data']
    assert len(res_desc) == len(res_asc), f'升序与降序数目不一样, title_uuid:{title_uuid}'
    res_asc = reversed(res_asc)
    for i, item in enumerate(res_asc):
        assert res_desc[i]['name'] == item['name'], '升序与降序对比不一致'


def query_title_shows_order_by_kdm_status(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    params = '{"title_uuid":"' + title_uuid + '"}'
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"kdm_status": "desc"}').text)
    res_desc = response['data']
    response = json.loads(title_client.query_title_show(params, context.token, order_by='{"kdm_status": "asc"}').text)
    res_asc = response['data']
    assert len(res_desc) == len(res_asc), f'升序与降序数目不一样, title_uuid:{title_uuid}'
    res_asc = reversed(res_asc)
    for i, item in enumerate(res_asc):
        assert res_desc[i]['name'] == item['name'], '升序与降序对比不一致'


def query_title_shows_filter_state(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)
    # 未匹配的场次
    params = '{"title_uuid":"' + title_uuid + '", "states":["unassigned"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_unassigned = response['data']
    # 已被sw匹配的场次
    params = '{"title_uuid":"' + title_uuid + '", "states":["assigned_in_sw"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_assigned_in_sw = response['data']
    # 已被producer匹配的场次
    params = '{"title_uuid":"' + title_uuid + '", "states":["assigned_in_producer"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_assigned_in_producer = response['data']
    # 已被sw匹配但未被producer匹配的场次
    params = '{"title_uuid":"' + title_uuid + '", "states":["unassigned", "assigned_in_sw"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_assigned_in_sw_but_pro = response['data']
    # 已被sw和producer匹配的场次
    params = '{"title_uuid":"' + title_uuid + '", "states":["assigned_in_sw", "assigned_in_producer"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_assigned_in_both = response['data']
    m = {}
    for show in shows:
        pos_uuid = show['pos_uuid']
        m[pos_uuid] = show['state']

    def compare(res: list, _type: str):
        for data in res:
            data_state = data['state']
            show_state = m[data['pos_uuid']]
            assert data_state == show_state, f'{_type}:状态不一致:data_state={data_state}, show_state={show_state}'

    # 对比各种res
    compare(res_unassigned, 'res_unassigned')
    compare(res_assigned_in_sw, 'res_assigned_in_sw')
    compare(res_assigned_in_sw_but_pro, 'res_assigned_in_sw_but_pro')
    compare(res_assigned_in_producer, 'res_assigned_in_producer')
    compare(res_assigned_in_both, 'res_assigned_in_both')


def query_title_shows_filter_date_time(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    start_date = str(datetime.date.today() + datetime.timedelta(days=1))
    end_date = str(datetime.date.today() + datetime.timedelta(days=3))
    # now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_time = '11:10'
    end_time = '11:20'
    # 大于start_date的场次
    params = '{"title_uuid":"' + title_uuid + '", "start_date": "' + start_date + '", "start_time": "' + start_time + '"}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_start = response['data']
    # 小于end_date的场次
    params = '{"title_uuid":"' + title_uuid + '", "end_date": "' + end_date + '", "end_time": "' + end_time + '"}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_end = response['data']
    # 大于start_date且小于end_date的场次
    params = '{"title_uuid":"' + title_uuid + '", "start_date": "' + start_date + '", "start_time": "' + start_time + '", "end_time": "' + "11:50" + '"}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_start_end = response['data']

    def to_unix_stamp(date_str):
        timeArray = time.strptime(date_str, "%Y-%m-%d")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp * 1000

    s = set()
    for show in shows:
        s.add(show['pos_uuid'])

    def compare(res: list, _type: str):
        for data in res:
            assert data['pos_uuid'] in s, f'{_type}:不一致:show_list里不存在pos_uuid:{data["pos_uuid"]}'

    # start_unix = to_unix_stamp(start_date)
    # end_unix = to_unix_stamp(end_date)
    compare(res_start, 'res_start')
    # compare(res_end, 'res_end')
    compare(res_start_end, 'res_start_end')


def query_title_shows_filter_playback_modes(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # 2d的场次
    params = '{"title_uuid":"' + title_uuid + '", "playback_modes":["2d"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_2d = response['data']
    # 3d的场次
    params = '{"title_uuid":"' + title_uuid + '", "playback_modes":["3d"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_3d = response['data']
    # 2d和3d的场次
    params = '{"title_uuid":"' + title_uuid + '", "playback_modes":["2d","3d"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_2d_3d = response['data']

    m = {}
    for show in shows:
        m[show['pos_uuid']] = show

    def compare(res: list, _type: str):
        for data in res:
            pos_uuid = data['pos_uuid']
            m_pos_show_attributes = m[pos_uuid]['pos_show_attributes']
            pos_show_attributes = data['pos_show_attributes']
            if m_pos_show_attributes is None:
                assert pos_show_attributes is None, f"m_pos_show_attributes为None, 但pos_show_attributes为:{pos_show_attributes}"
                continue
            assert len(m_pos_show_attributes) == len(pos_show_attributes), \
                f'{_type}:pos_show_attributes长度不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'
            for i, attr in enumerate(pos_show_attributes):
                assert attr == m_pos_show_attributes[i], \
                    f'{_type}:pos_show_attributes不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'

    compare(res_2d, 'res_2d')
    compare(res_3d, 'res_3d')
    compare(res_2d_3d, 'res_2d_3d')


def query_title_shows_filter_experience(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # dbox的场次
    params = '{"title_uuid":"' + title_uuid + '", "experiences":["dbox"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_dbox = response['data']
    # imax的场次
    params = '{"title_uuid":"' + title_uuid + '", "experiences":["imax"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_imax = response['data']
    # 2d和3d的场次
    params = '{"title_uuid":"' + title_uuid + '", "experiences":["dbox","imax"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_dbox_imax = response['data']

    m = {}
    for show in shows:
        m[show['pos_uuid']] = show

    def compare(res: list, _type: str):
        for data in res:
            pos_uuid = data['pos_uuid']
            m_pos_show_attributes = m[pos_uuid]['pos_show_attributes']
            pos_show_attributes = data['pos_show_attributes']
            if m_pos_show_attributes is None:
                assert pos_show_attributes is None, f"m_pos_show_attributes为None, 但pos_show_attributes为:{pos_show_attributes}"
                continue
            assert len(m_pos_show_attributes) == len(pos_show_attributes), \
                f'{_type}:pos_show_attributes长度不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'
            for i, attr in enumerate(pos_show_attributes):
                assert attr == m_pos_show_attributes[i], \
                    f'{_type}:pos_show_attributes不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'

    compare(res_dbox, 'res_dbox')
    compare(res_imax, 'res_imax')
    compare(res_dbox_imax, 'res_dbox_imax')


def query_title_shows_filter_other_attrs(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # customs的场次
    params = '{"title_uuid":"' + title_uuid + '", "customs":["customs"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_customs = response['data']
    # customs1和customs2的场次
    params = '{"title_uuid":"' + title_uuid + '", "customs":["customs1","customs2"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_customs1_customs2 = response['data']

    m = {}
    for show in shows:
        m[show['pos_uuid']] = show

    def compare(res: list, _type: str):
        for data in res:
            pos_uuid = data['pos_uuid']
            m_pos_show_attributes = m[pos_uuid]['pos_show_attributes']
            pos_show_attributes = data['pos_show_attributes']
            if m_pos_show_attributes is None:
                assert pos_show_attributes is None, f"m_pos_show_attributes为None, 但pos_show_attributes为:{pos_show_attributes}"
                continue
            assert len(m_pos_show_attributes) == len(pos_show_attributes), \
                f'{_type}:pos_show_attributes长度不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'
            for i, attr in enumerate(pos_show_attributes):
                assert attr == m_pos_show_attributes[i], \
                    f'{_type}:pos_show_attributes不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'

    compare(res_customs, 'res_customs')
    compare(res_customs1_customs2, 'res_customs1_customs2')


def query_title_shows_filter_lang(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # en的场次
    params = '{"title_uuid":"' + title_uuid + '", "audio_langs":["en"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_en = response['data']
    # en和zh的场次
    params = '{"title_uuid":"' + title_uuid + '", "audio_langs":["en", "zh"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_en_zh = response['data']

    m = {}
    for show in shows:
        m[show['pos_uuid']] = show

    def compare(res: list, _type: str):
        for data in res:
            pos_uuid = data['pos_uuid']
            m_pos_show_attributes = m[pos_uuid]['pos_show_attributes']
            pos_show_attributes = data['pos_show_attributes']
            if m_pos_show_attributes is None:
                assert pos_show_attributes is None, f"m_pos_show_attributes为None, 但pos_show_attributes为:{pos_show_attributes}"
                continue
            assert len(m_pos_show_attributes) == len(pos_show_attributes), \
                f'{_type}:pos_show_attributes长度不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'
            for i, attr in enumerate(pos_show_attributes):
                assert attr == m_pos_show_attributes[i], \
                    f'{_type}:pos_show_attributes不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'

    compare(res_en, 'res_en')
    compare(res_en_zh, 'res_en_zh')


def query_title_shows_filter_subtitle_lang(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # en的场次
    params = '{"title_uuid":"' + title_uuid + '", "subtitle_langs":["en"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_en = response['data']
    # en和zh的场次
    params = '{"title_uuid":"' + title_uuid + '", "subtitle_langs":["en","zh"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_en_zh = response['data']

    m = {}
    for show in shows:
        m[show['pos_uuid']] = show

    def compare(res: list, _type: str):
        for data in res:
            pos_uuid = data['pos_uuid']
            m_pos_show_attributes = m[pos_uuid]['pos_show_attributes']
            pos_show_attributes = data['pos_show_attributes']
            if m_pos_show_attributes is None:
                assert pos_show_attributes is None, f"m_pos_show_attributes为None, 但pos_show_attributes为:{pos_show_attributes}"
                continue
            assert len(m_pos_show_attributes) == len(pos_show_attributes), \
                f'{_type}:pos_show_attributes长度不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'
            for i, attr in enumerate(pos_show_attributes):
                assert attr == m_pos_show_attributes[i], \
                    f'{_type}:pos_show_attributes不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'

    compare(res_en, 'res_en')
    compare(res_en_zh, 'res_en_zh')


def query_title_shows_filter_complex_name(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # sw03-test的场次
    params = '{"title_uuid":"' + title_uuid + '", "complex_names":["sw03-test(Cineworld 03T)"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_sw03 = response['data']
    # 不存在的场次
    params = '{"title_uuid":"' + title_uuid + '", "complex_names":["sw03-test(Cineworld 03T)","sw01-test(agent on k8s-test)"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_dne = response['data']

    s = set()
    for show in shows:
        s.add(show['pos_uuid'])

    def compare(res: list, _type: str):
        for data in res:
            assert data['pos_uuid'] in s, f'{_type}:不一致:show_list里不存在pos_uuid:{data["pos_uuid"]}'

    compare(res_sw03, 'res_sw03')
    compare(res_dne, 'res_dne')


def query_title_shows_filter_subtitle_lang(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # en的场次
    params = '{"title_uuid":"' + title_uuid + '", "subtitle_langs":["en"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_en = response['data']
    # en和zh的场次
    params = '{"title_uuid":"' + title_uuid + '", "subtitle_langs":["en","zh"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_en_zh = response['data']

    m = {}
    for show in shows:
        m[show['pos_uuid']] = show

    def compare(res: list, _type: str):
        for data in res:
            pos_uuid = data['pos_uuid']
            m_pos_show_attributes = m[pos_uuid]['pos_show_attributes']
            pos_show_attributes = data['pos_show_attributes']
            if m_pos_show_attributes is None:
                assert pos_show_attributes is None, f"m_pos_show_attributes为None, 但pos_show_attributes为:{pos_show_attributes}"
                continue
            assert len(m_pos_show_attributes) == len(pos_show_attributes), \
                f'{_type}:pos_show_attributes长度不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'
            for i, attr in enumerate(pos_show_attributes):
                assert attr == m_pos_show_attributes[i], \
                    f'{_type}:pos_show_attributes不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'

    compare(res_en, 'res_en')
    compare(res_en_zh, 'res_en_zh')


def query_title_shows_filter_complex_name(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # sw03-test的场次
    params = '{"title_uuid":"' + title_uuid + '", "complex_names":["sw03-test(Cineworld 03T)"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_sw03 = response['data']
    # 不存在的场次
    params = '{"title_uuid":"' + title_uuid + '", "complex_names":["sw03-test(Cineworld 03T)","sw01-test(agent on k8s-test)"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_dne = response['data']

    s = set()
    for show in shows:
        s.add(show['pos_uuid'])

    def compare(res: list, _type: str):
        for data in res:
            assert data['pos_uuid'] in s, f'{_type}:不一致:show_list里不存在pos_uuid:{data["pos_uuid"]}'

    compare(res_sw03, 'res_sw03')
    compare(res_dne, 'res_dne')


def query_title_shows_filter_screen(context):
    title_uuid = context.title['uuid']
    shows = context.title_shows
    title_client = TitleClient(context.title_url)

    # sw03-test的场次
    params = '{"title_uuid":"' + title_uuid + '", "screen_show_attributes":["HI"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_hi = response['data']
    # 不存在的场次
    params = '{"title_uuid":"' + title_uuid + '", "screen_show_attributes":["HI", "5.1"]}'
    response = json.loads(title_client.query_title_show(params, context.token).text)
    res_hi_51 = response['data']

    m = {}
    for show in shows:
        m[show['pos_uuid']] = show

    def compare(res: list, _type: str):
        for data in res:
            pos_uuid = data['pos_uuid']
            m_pos_show_attributes = m[pos_uuid]['pos_show_attributes']
            pos_show_attributes = data['pos_show_attributes']
            if m_pos_show_attributes is None:
                assert pos_show_attributes is None, f"m_pos_show_attributes为None, 但pos_show_attributes为:{pos_show_attributes}"
                continue
            assert len(m_pos_show_attributes) == len(pos_show_attributes), \
                f'{_type}:pos_show_attributes长度不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'
            for i, attr in enumerate(pos_show_attributes):
                assert attr == m_pos_show_attributes[i], \
                    f'{_type}:pos_show_attributes不一致, title_uuid:{title_uuid}, pos_uuid:{pos_uuid}'

    compare(res_hi, 'res_hi')
    compare(res_hi_51, 'res_hi_51')


def query_a_title_has_content(context):
    # query_title(context, "{}", Fa?lse)
    title_client = TitleClient(context.title_url)
    res = title_client.query_title(context.token)
    res_all = json.loads(res.text)['data']
    context.title_list = res_all
    res = context.title_list
    assert res is not None and len(res) > 0, '找不到任何title列表'
    title_client = TitleClient(context.posuuid_url)
    # 遍历直到有content列表为止
    for title in res:
        title_uuid = title['uuid']
        response = json.loads(title_client.query_title_content(title_uuid, context.token).text)
        if response['code'] == 200 and 'data' in response and response['data'] is not None and len(
                response['data']) > 0:
            context.title = title
            context.title_contents = response['data']
            return
    raise RuntimeError('找不到任何含有content的title')


def query_title_content_filter_name(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 精确
    params = {'search_title': 'ABC | TEST'}
    res = json.loads(title_client.query_title_content(title_uuid, context.token, params=params).text)
    res_exact = res['data']
    # 模糊
    params = {'search_title': 'ABC'}
    res = json.loads(title_client.query_title_content(title_uuid, context.token, params=params).text)
    res_vague = res['data']
    # 不存在的
    params = {'search_title': 'dne EExxiisstt'}
    res = json.loads(title_client.query_title_content(title_uuid, context.token, params=params).text)
    res_dne = res['data']

    assert len(res_dne) == 0, f'搜索不存在的title_content返回了结果, title_uuid:{title_uuid}'

    m = {}
    for item in contents:
        m[item['uuid']] = item['title']

    for exact in res_exact:
        assert m[exact['uuid']] == exact['title'], f'精确查询title_content不一致, title_uuid:{title_uuid}'

    for vague in res_vague:
        assert m[vague['uuid']].find(vague['title']) != -1, f'模糊查询title_content不一致, title_uuid:{title_uuid}'


def query_title_content_filter_content_type(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"content_types":["feature"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_fea = res['data']
    params = '{"content_types":["feature","advertisement"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_fea_adv = res['data']
    params = '{"content_types":["rating","other"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_rat_oth = res['data']

    def compare(res: list, correct_content_types):
        for data in res:
            content_type = data['content_kind']
            count = 0
            for correct_content_type in correct_content_types:
                if correct_content_type == content_type:
                    count += 1
            assert count > 0, f'没有匹配的title_content,但却有匹配的结果,title_uuid:{title_uuid}, 参数:{correct_content_types}'

    compare(res_fea, ["feature"])
    compare(res_fea_adv, ["feature", "advertisement"])
    compare(res_rat_oth, ["rating", "other"])


def query_title_content_filter_status(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"status":["inuse"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    # print(f"原始结果：%s" % json.dumps(res))
    res_fea = res['data']
    params = '{"status":["unuse"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_fea_adv = res['data']
    params = '{"status":["inuse", "unuse"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_rat_oth = res['data']

    def compare(res: list, correct_status):
        for data in res:
            # print(f"输出status:%s" % data['status'])
            statu = data['status']
            count = 0
            for correct_statu in correct_status:
                if correct_statu == statu:
                    count += 1
            assert count > 0, f'没有匹配的title_content,但却有匹配的结果,title_uuid:{title_uuid}, 参数:{correct_status}'

    compare(res_fea, ["inuse"])
    compare(res_fea_adv, ["unuse"])
    compare(res_rat_oth, ["inuse", "unuse"])


def query_title_content_filter_date(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"begin_date":1568044800000}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_begin = res['data']
    params = '{"end_date":15689087999990}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_end = res['data']
    params = '{"begin_date":1568044800000,"end_date":15689087999990}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_begin_end = res['data']

    def compare(res: list, start=None, end=None):
        for data in res:
            date = data['created']
            if start is not None:
                assert date >= start, f'查询的content超过开始时间:{date}, 参数:start:{start}, title_uuid:{title_uuid}'
            if end is not None:
                assert date <= end, f'查询的content超过结束时间:{date}, 参数:end:{end}, title_uuid:{title_uuid}'

    compare(res_begin, start=1568044800000)
    compare(res_end, start=None, end=15689087999990)
    compare(res_begin_end, start=1568044800000, end=15689087999990)


def query_title_content_filter_playback_modes(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"playback_modes":["2d"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_2d = res['data']
    params = '{"playback_modes":["3d"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_3d = res['data']
    params = '{"playback_modes":["2d","3d"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_2d_3d = res['data']

    m = {}
    for item in contents:
        m[item['uuid']] = item['title']

    def compare(res: list, correct_modes):
        for data in res:
            assert data[
                       'uuid'] in m, f'按playback_mode查询出的content不符合:title_uuid:{title_uuid}, playback_modes:{correct_modes}'

    compare(res_2d, ["2d"])
    compare(res_3d, ["3d"])
    compare(res_2d_3d, ["2d", "3d"])


def query_title_content_filter_experiences(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"experiences":["DBOX"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_dbox = res['data']
    params = '{"experiences":["IMAX"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_imax = res['data']
    params = '{"experiences":["DBOX","IMAX"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_dbox_imax = res['data']

    m = {}
    for item in contents:
        m[item['uuid']] = item['title']

    def compare(res: list, correct_experiences):
        for data in res:
            assert data[
                       'uuid'] in m, f'按experiences查询出的content不符合:title_uuid:{title_uuid}, experiences:{correct_experiences}'

    compare(res_dbox, ["DBOX"])
    compare(res_imax, ["IMAX"])
    compare(res_dbox_imax, ["DBOX", "IMAX"])


def query_title_content_filter_aspect_ratios(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"aspect_ratios":["flat"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_flat = res['data']
    params = '{"aspect_ratios":["scope"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_scope = res['data']
    params = '{"aspect_ratios":["scope","full"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_scope_full = res['data']

    m = {}
    for item in contents:
        m[item['uuid']] = item['title']

    def compare(res: list, correct_aspect_ratios):
        for data in res:
            assert data[
                       'uuid'] in m, f'按experiences查询出的content不符合:title_uuid:{title_uuid}, aspect_ratios:{correct_aspect_ratios}'

    compare(res_flat, ["flat"])
    compare(res_scope, ["scope"])
    compare(res_scope_full, ["scope", "full"])


def query_title_content_filter_audio_formats(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"audio_formats":["5.1"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_51 = res['data']
    params = '{"audio_formats":["7.1"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_71 = res['data']
    params = '{"audio_formats":["5.1","7.1"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_51_71 = res['data']

    m = {}
    for item in contents:
        m[item['uuid']] = item['title']

    def compare(res: list, correct_audio_formats):
        for data in res:
            audio_formats = data['format']
            count = 0
            for audio_format in audio_formats:
                for correct_audio_format in correct_audio_formats:
                    if correct_audio_format == audio_format:
                        count += 1
            assert count > 0, f'没有匹配的title_content,但却有匹配的结果,title_uuid:{title_uuid}, 参数:{correct_audio_formats}'

    compare(res_51, ["5.1"])
    compare(res_71, ["7.1"])
    compare(res_51_71, ["5.1", "7.1"])


def query_title_content_filter_audio_langs(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"audio_langs":["en"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_en = res['data']
    params = '{"audio_langs":["zh"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_zh = res['data']
    params = '{"audio_langs":["en","zh"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_en_zh = res['data']

    m = {}
    for item in contents:
        m[item['uuid']] = item['title']

    def compare(res: list, correct_audio_langs):
        for data in res:
            audio_lang = data['language']
            count = 0
            for correct_audio_lang in correct_audio_langs:
                if correct_audio_lang == audio_lang:
                    count += 1
            assert count > 0, f'没有匹配的title_content,但却有匹配的结果,title_uuid:{title_uuid}, 参数:{correct_audio_langs}'

    compare(res_en, ["en"])
    compare(res_zh, ["zh"])
    compare(res_en_zh, ["en", "zh"])


def query_title_content_filter_subtitle_langs(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"subtitle_langs":["en"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_en = res['data']
    params = '{"subtitle_langs":["zh"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_zh = res['data']
    params = '{"subtitle_langs":["en","zh"]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_en_zh = res['data']

    m = {}
    for item in contents:
        m[item['uuid']] = item['title']

    def compare(res: list, correct_subtitle_langs):
        for data in res:
            audio_lang = data['language']
            count = 0
            for correct_audio_lang in correct_subtitle_langs:
                if correct_audio_lang == audio_lang:
                    count += 1
            assert count > 0, f'没有匹配的title_content,但却有匹配的结果,title_uuid:{title_uuid}, 参数:{correct_subtitle_langs}'

    compare(res_en, ["en"])
    compare(res_zh, ["zh"])
    compare(res_en_zh, ["en", "zh"])


def query_title_content_filter_rating(context):
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    # 按各种分类查找
    params = '{"ratings":[{"territoryName":"UK","value":"PG"}]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_pg = res['data']
    params = '{"ratings":[{"territoryName":"UK","value":"PG"},{"territoryName":"UK","value":"15"}]}'
    res = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_pg_15 = res['data']

    m = {}
    for item in contents:
        m[item['uuid']] = item['title']

    def compare(res: list, correct_ratings):
        for i in correct_ratings:
            # print(f"输出i：%s" % i)
            # print(type(i))
            # print(f"输出key：%s" % i['territoryName'])
            i.update({'territory': i.pop('territoryName')})
            # print(f"输出修改后的key：%s" % i['territory'])
            i.update({'rating': i.pop('value')})
        print(f"输出correct_ratings：%s" % correct_ratings)
        # print(type(correct_ratings))
        for data in res:
            ratings = data['rating']
            if 'conflictRatings' in ratings[0]:
                del ratings[0]["conflictRatings"]
            # print("RATINGIS:", ratings)
            count = 0
            for rating in ratings:
                for correct_rating in correct_ratings:
                    print(f"入参correct_rating：%s" % correct_rating)
                    if correct_rating == rating:
                        count += 1
                    print(f"count的数量：%s" % count)
            assert count > 0, f'没有匹配的title_content,但却有匹配的结果,title_uuid:{title_uuid}, 参数:{correct_ratings}'

    compare(res_pg, [{"territoryName": "UK", "value": "PG"}])
    compare(res_pg_15, [{"territoryName": "UK", "value": "PG"}, {"territoryName": "UK", "value": "15"}])


def query_title_content_filter_complex_names(context, not_a_complex_uuid, not_a_complex_name):
    """                               暂时弃用，由只用complex name进行查询，修改为用complex name和 complexUUID双重查询验证   2022.2
    title_uuid = context.title['uuid']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)

    p_session = context.producer_view_session
    res = p_session.execute(f'''
        SELECT DISTINCT(cp.uuid),cp.content_name,cd.`name` 
        FROM cpl_locations_mapping clm,cpl_data cp,title_cpl_mapping tcm,complex_data cd  
        WHERE clm.cpl_uuid = cp.uuid 
        AND clm.complex_uuid = cd.uuid 
        AND tcm.cpl_uuid = cp.uuid 
        AND content_kind = 'feature' 
        AND tcm.title_uuid = '{title_uuid}';
        ''')
    rm = res.fetchone()
    cpl_uuid = rm[0]
    complex_name = rm[2]

    res = p_session.execute(f'''
        SELECT DISTINCT(cp.uuid),cp.content_name,cd.`name` 
        FROM cpl_locations_mapping clm,cpl_data cp,title_cpl_mapping tcm,complex_data cd  
        WHERE clm.cpl_uuid = cp.uuid 
        AND clm.complex_uuid = cd.uuid 
        AND tcm.cpl_uuid = cp.uuid 
        AND content_kind = 'feature' 
        AND cp.uuid = '{cpl_uuid}' 
        AND tcm.title_uuid = '{title_uuid}';
        ''')

    assert_count = contents[0]['complex_count']
    count = 0
    rm = res.fetchall()
    for item in rm:
        count += 1
    assert count == assert_count, f'查询的数量不一致, title_uuid:{title_uuid}, cpl_uuid:{cpl_uuid}'

    # 按各种分类查找
    params = '{"complex_names":["'+complex_name+'"]}'
    response = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_cn = response['data']
    params = '{"complex_names":["a_not exist_complex"]}'
    response = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
    res_dne = response['data']

    flag = False
    for item in rm:
        if cpl_uuid == item['uuid']:
            assert res_cn[0]['uuid'] == cpl_uuid, f'cpl_uuid不一致'
            flag = True
    assert flag, f'找不到有关的title_content数据:{title_uuid}, cpl_uuid:{cpl_uuid}'
    assert len(res_dne) == 0, f'查询不存在的数据，但返回有结果title_uuid:{title_uuid}, complex_name:{complex_name}'
    """

    title_uuid = context.title['uuid']
    title_name = context.title['name']
    contents = context.title_contents
    title_client = TitleClient(context.posuuid_url)
    site_client = SiteClient(context.posuuid_url)
    content_client = Content(context.posuuid_url)

    title_cpl = []
    title_cpls = {''}
    res = site_client.query_site('{}', context.token)
    res = res.json()['data']

    for detail in res:
        complex_name = detail['name']
        complex_uuid = detail['uuid']
        filter = '{"complex_uuids":["' + complex_uuid + '"]}'
        res = json.loads(
            content_client.query_content_by_title_complex(context.token, filter=filter, search_title=title_name).text)
        for i in range(len(res['data'])):
            cpl_uuid = res['data'][i]['uuid']
            title_cpl.append(cpl_uuid)
            title_cpls.update(title_cpl)

        params = '{"complex_uuids":["' + complex_uuid + '"]}'
        response = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
        res_cn = response['data']
        params = '{"complex_uuids":["' + not_a_complex_uuid + '"]}'
        response = json.loads(title_client.query_title_content(title_uuid, context.token, filter=params).text)
        res_ncn = response['data']
        query_cpls = []
        if res_ncn:
            flag = False
            assert flag, f'找到影院{not_a_complex_uuid}相关的CPL'

        for cpl_detail in res_cn:
            for cpl in title_cpls:
                for i in range(len(title_cpls)):
                    if cpl_detail['uuid'] == cpl:
                        query_cpls.append(cpl_detail['uuid'])
                    elif cpl == '':
                        flag = True
                        assert flag, f'查询CPl与实际CPl对应不上，实际cpl为：{title_cpls}，查询所得cpl：{query_cpls}'
                    else:
                        flag = False
                        assert flag, f'查询CPl与实际CPl对应不上，实际cpl为：{title_cpls}，查询所得cpl：{query_cpls}'
                    break
                break
