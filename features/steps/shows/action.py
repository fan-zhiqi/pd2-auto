#!/usr/bin/python
# -*-coding:utf-8 -*-

import datetime
import logging
import jsonpath

from features.steps.shows.kafka_util.show_client import ShowClient


def query_shows_all(context, start_time, screen_show_attributes=[], search_name='', states=[], start_date='',
                    match_title_bool='' and bool):
    '''可以根据状态查询列表"unassigned","assigned_in_sw","assigned_in_producer","automatically","pending"
    return的context:一个场次信息包括show_name_list，pos_uuid
    '''
    a = datetime.datetime.now().strftime('%Y-%m-%d')
    res = ShowClient(context.producer_view_url).query_show(context.token, states=states, start_time=start_time,
                                                           search_name=search_name,
                                                           screen_show_attributes=screen_show_attributes,
                                                           match_title_bool=match_title_bool, start_date=a)
    context.resp = res.json()
    return context.resp


def query_no_assigned_have_show_attr(context):
    '''filter: {"states":["unassigned"],"screen_show_attributes":["2D","3D","4D","4DX","CC","CGS"]}'''

    a = (datetime.datetime.now() + datetime.timedelta(hours=4)).strftime('%H:%M')
    query_shows_all(context, start_time=a, states=["unassigned"],
                    screen_show_attributes=["2D", "3D", "4D", "4DX", "CC", "CGS", "CINITY", "DBOX", "DVIS", "HFR", "HI",
                                            "HOH", "IMX", "LNG", "MX4D", "SCREENX", "SUB", "VI", "Private"])
    context.all_show_name_pos_uuid_list = []
    for i in context.resp['data']:
        if i['pos_show_attributes'] != []:
            context.all_show_name_pos_uuid_list.append(
                {'name': i['name'], 'pos_uuid': i['pos_uuid'], 'pos_show_attributes': i['pos_show_attributes']})
    logging.info(context.all_show_name_pos_uuid_list)
    context.a = context.all_show_name_pos_uuid_list
    context.pos_one_name_str = context.all_show_name_pos_uuid_list[0]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = context.all_show_name_pos_uuid_list[0]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)
    context.pos_show_attributes_list = context.all_show_name_pos_uuid_list[0]['pos_show_attributes']
    return context.resp


def query_no_assigned_have_show_attr1(context):
    '''filter: {"states":["unassigned"],"screen_show_attributes":["2D","3D","4D","4DX","CC","CGS"]}'''

    a = (datetime.datetime.now() + datetime.timedelta(hours=4)).strftime('%H:%M')
    query_shows_all(context, start_time=a, states=["unassigned"],
                    screen_show_attributes=["2D", "3D", "4D", "4DX", "CC", "CGS", "CINITY", "DBOX", "DVIS", "HFR", "HI",
                                            "HOH", "IMX", "LNG", "MX4D", "SCREENX", "SUB", "VI", "Private"])
    context.all_show_name_pos_uuid_list = []
    for i in context.resp['data']:
        if i['pos_show_attributes'] != []:
            context.all_show_name_pos_uuid_list.append(
                {'name': i['name'], 'pos_uuid': i['pos_uuid'], 'pos_show_attributes': i['pos_show_attributes']})
    a = []
    for i in context.all_show_name_pos_uuid_list:
        b = jsonpath.jsonpath(a, '$..name')
        if b:
            if i['name'] in b:
                continue
            else:
                a.append(i)
        else:
            a.append(i)
            continue
    context.a = a
    context.pos_one_name_str = a[1]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = a[1]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)
    context.pos_show_attributes_list = a[1]['pos_show_attributes']
    return context.resp


def query_no_assigned_have_show_attr2(context):
    '''filter: {"states":["unassigned"],"screen_show_attributes":["2D","3D","4D","4DX","CC","CGS"]}'''

    a = (datetime.datetime.now() + datetime.timedelta(hours=4)).strftime('%H:%M')
    query_shows_all(context, start_time=a, states=["unassigned"],
                    screen_show_attributes=["2D", "3D", "4D", "4DX", "CC", "CGS", "CINITY", "DBOX", "DVIS", "HFR", "HI",
                                            "HOH", "IMX", "LNG", "MX4D", "SCREENX", "SUB", "VI", "Private"])
    context.all_show_name_pos_uuid_list = []
    for i in context.resp['data']:
        if i['pos_show_attributes'] != []:
            context.all_show_name_pos_uuid_list.append(
                {'name': i['name'], 'pos_uuid': i['pos_uuid'], 'pos_show_attributes': i['pos_show_attributes']})
    a = []
    for i in context.all_show_name_pos_uuid_list:
        b = jsonpath.jsonpath(a, '$..name')
        if b:
            if i['name'] in b:
                continue
            else:
                a.append(i)
        else:
            a.append(i)
            continue
    context.a = a
    context.pos_one_name_str = a[-1]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = a[-1]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)
    context.pos_show_attributes_list = a[-1]['pos_show_attributes']
    return context.resp


def query_shows_match_title(context, search_name='', states=[], start_date='', match_title_bool='' and bool):
    '''可以根据状态查询列表"unassigned","assigned_in_sw","assigned_in_producer","automatically","pending"
        return的context:一个场次信息包括show_name_list，pos_uuid
        '''
    b = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%H:%M')
    res = ShowClient(context.producer_view_url).query_show(context.token, states=states, start_time=b,
                                                           search_name=search_name,
                                                           match_title_bool=match_title_bool, start_date=start_date)
    context.resp = res.json()
    a = []
    for i in context.resp['data']:
        if i['pos_show_attributes'] == []:
            a.append(i['name'])
    a = set(a)  # 形成set类型
    a = list(a)
    if len(a) >= 3:
        context.pos_name_list = a[1:2]
    else:
        context.pos_name_list = a
    context.pos_one_name_str = a[0]
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    return context.resp


def query_shows_match_title1(context, search_name='', states=[], start_date='', match_title_bool='' and bool):
    '''可以根据状态查询列表"unassigned","assigned_in_sw","assigned_in_producer","automatically","pending"
        return的context:一个场次信息包括show_name_list，pos_uuid
        '''
    b = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%H:%M')
    res = ShowClient(context.producer_view_url).query_show(context.token, states=states, start_time=b,
                                                           search_name=search_name,
                                                           match_title_bool=match_title_bool, start_date=start_date)
    context.resp = res.json()
    a = []
    for i in context.resp['data']:
        if i['pos_show_attributes'] == []:
            a.append(i['name'])
    a = set(a)  # 形成set类型
    a = list(a)
    if len(a) >= 3:
        context.pos_name_list = a[1:2]
    else:
        context.pos_name_list = a
    context.pos_one_name_str = a[3]
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    return context.resp


def query_shows_get_pos_uuid(context):
    a = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime('%H:%M')
    query_shows_all(context, start_time=a, states=["unassigned"])
    context.all_show_name_pos_uuid_list = []
    for i in context.resp['data']:
        if i['pos_show_attributes'] == []:
            context.all_show_name_pos_uuid_list.append({'name': i['name'], 'pos_uuid': i['pos_uuid']})
    # context.pos_one_name_str = context.all_show_name_pos_uuid_list[0]['name']
    # context.pos_one_name_list = []
    # context.pos_one_name_list.append(context.pos_one_name_str)
    # context.pos_uuid = context.all_show_name_pos_uuid_list[0]['pos_uuid']
    # context.pos_uuid_list = []
    # context.pos_uuid_list.append(context.pos_uuid)
    # logging.info(context.all_show_name_pos_uuid_list)
    return context.resp


def macth_title(context, show_name_list, title_uuid):
    data = {
        'pos_name_list': show_name_list,
        'uuid': title_uuid
    }
    res = ShowClient(context.title_url).match_title(context.token, data=data)
    context.resp = res.json()
    return context.resp


def unmacth_title(context, show_name_list, title_uuid):
    data = [{
        'pos_name_list': show_name_list,
        'uuid': title_uuid
    }]
    res = ShowClient(context.title_url).unmatch_title(context.token, data=data)
    context.resp = res.json()
    return context.resp


def assigned_shows(context, playlist_uuid, pos_uuid_list):
    res = ShowClient(context.producer_view_url).assigned(context.token, playlist_uuid, pos_uuid_list)
    context.resp = res.json()
    return context.resp


def unassigned_shows(context, pos_uuid_list):
    res = ShowClient(context.producer_view_url).unassigned(context.token, pos_uuid_list)
    context.resp = res.json()
    return context.resp


def qurey_show_detail(context, pos_uuid):
    res = ShowClient(context.producer_view_url).query_show_detail(context.token, pos_uuid)
    context.resp = res.json()
    context.state = jsonpath.jsonpath(context.resp, '$..state')[0]
    return context.resp
