import json
import random

import allure
import jsonpath

from features.steps.content.content_utils.content_client import Content
from tools.logger import GetLogger

log = GetLogger().get_logger()


def create_content(context, content_title_text):
    '''只输入名称创建cpl
    return中只返回了code，未返回uuid
    '''
    random_content_title_text = content_title_text + str(random.randint(1300000000, 14000000000))
    context.content_title_text = random_content_title_text
    content_client = Content(context.producer_view_url)
    log.info('请求参数为{}'.format(context.content_title_text))
    res = content_client.create_content(context.token, context.content_title_text)
    context.resp = res.json()
    return context.resp


def create_repeat_content(context, content_title_text):
    '''创建重复名称cpl'''
    context_client = Content(context.producer_view_url)
    res = context_client.query_content(context.token, content_title_text)
    res_all = res.json().get('data')
    title = res_all[0]['content_title_text']
    log.info('查询列表中第一个title的名{}'.format(title))
    context.content_title_text = content_title_text
    if title == content_title_text:
        res2 = context_client.create_content(context.token, content_title_text)
    else:
        res = context_client.create_content(context.token, content_title_text)
        res2 = context_client.create_content(context.token, content_title_text)
    context.resp = res2.json()
    return context.resp


def edit_content_attr(context, cpl_uuid, access_audio='', access_subtitles='', audio='', content_kind='', dimension='',
                      duration_numerator='' or 7200, edit_rate='',
                      facility='',
                      language='', resolution='', special_effect='', studio='', subtitles='', visual_format=''):
    '''编辑content的属性'''

    log.info(f'修改的cpl_uuid为{context.content_uuid}')
    b = str(random.randint(130000, 1400000))
    facility = facility + b
    language = language + b
    studio = studio + b
    data = {
        'access_audio': access_audio,
        'access_subtitles': access_subtitles,
        'audio': audio,
        'content_kind': content_kind,
        'dimension': dimension,
        'duration_numerator': duration_numerator,
        'edit_rate': edit_rate,
        'facility': facility,
        'language': language,
        'resolution': resolution,
        'special_effect': special_effect,
        'studio': studio,
        'subtitles': subtitles,
        'visual_format': visual_format
    }
    res = Content(context.producer_view_url).edit_content_attr_client(context.token, cpl_uuid=cpl_uuid, data=data)
    context.resp = res.json()
    return context.resp


def edit_content_offset_time(context, cpl_uuid,
                             modify_types='rolling_credit' or 'credit_offset' or 'hard_lock_offset' or 'screenwriter_credit_offset'):
    '''编辑content中的offset属性'''
    try:
        title_client = Content(context.producer_view_url)
        time = random.randint(1000, 7200000)
        res = title_client.edit_content_offset(context.token, cpl_uuid, time=time, modify_types=modify_types)
        context.resp = res.json()
        return context.resp
    except:
        '修改的時間大於縂時常'


def query_content_by_str(context, title: str):
    context.need_query_content_title = title
    res = Content(context.producer_view_url).query_content(context.token, search_title=context.need_query_content_title)
    context.resp = res.json()
    context.content_uuid = context.resp.get('data')[0]['uuid']
    return context.resp


def query_complex_content(context):
    res = Content(context.producer_view_url).query_all_content(context.token,num=1)
    a = res.json()
    for num in range(100):
        b = jsonpath.jsonpath(a, '$..placeholder')
        log.info(b)
        if False in b:
            for i in a['data']:
                if i['placeholder'] == False:
                    context.content_uuid = i['uuid']
                    break
        else:
            num+=1
            res = Content(context.producer_view_url).query_all_content(context.token, num)
            a = res.json()


