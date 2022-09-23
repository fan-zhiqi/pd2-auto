#!/usr/bin/python
# -*-coding:utf-8 -*-
import json
import logging
import time

import allure
import jsonpath
from behave import when
import features.steps.celery_steps.actions as celery_actions
import features.steps.s3.actions as s3_actions
import features.steps.api.actions as api_actions
import features.steps.playlist.actions as playlist_actions
from features.steps.shows.action import *
import features.steps.title.actions as title_actions
import features.steps.shows.action as show_actions
import features.steps.content.action as content_action
import features.steps.segment.action as segment_action
import features.steps.macro.action as macro_action


@when('"{actor}" uploads directory "{directory}" to s3 bucket "{bucket_name}"')
def upload_directory(context, actor, directory, bucket_name):
    s3_actions.upload_directory_to_s3_with_contents(
        context,
        actor,
        directory_name=directory,
        bucket_name=bucket_name
    )


@when('"{actor}" gains access to Producer Frontend as user "{email_address}" '
      'with password "{password}"')
def login_to_producer_frontend(context, actor, email_address, password):
    api_actions.login(context, actor, email_address, password)


@when('"{actor}" send kdm "{kdm_name}" to the kdm service with user '
      '"{user_name}"')
def send_kdm_to_kdm_service(context, actor, kdm_name, user_name):
    celery_actions.handle_asset_task(context, actor, user_name, kdm_name)


@when('"{actor}" assigns "{recipient_name}" to a '
      'device called "{alias_name}"')
def assigning_to_device(context, actor, recipient_name, alias_name):
    api_actions.assigning_kdm_to_device(
        context, actor, recipient_name, alias_name
    )


"""
---------------------------------title--------------------------------------
"""


@when('请求movie接口获取source_id')
def query_source_id(context):
    title_actions.query_movies_id(context)


@when('输入参数name:{name}和source时输入正确时获取title_uuid')
def create_title_case(context, name):
    title_actions.create_title(context, name)


@when('输入name为空,source_id不为空时')
def create_lack_name_title(context):
    title_actions.create_lack_name_title(context)


@when('输入非必填参数source_id为空name不为空时')
def create_lack_source_id_title(context):
    title_actions.create_lack_source_id_title(context)


@when('输入重复的{name}时source_id不变')
def create_repeat_name_title(context, name):
    title_actions.create_repeat_title(context, name)


"""
---------------------------------query_title---------------------------------
"""


@when('请求查询列表,并提取title_uuid_list')
def qurey_title_get_title_uuid_list(context):
    title_actions.query_title_by_str(context)


"""
---------------------------------create_placeholder_content---------------------------------
"""


@when('输入必填参数{content_title_text}创建cpl')
def creat_content(context, content_title_text):
    content_action.create_content(context, content_title_text)


@when('填写重复{content_title_text}时')
def create_repeat_content(context, content_title_text):
    content_action.create_repeat_content(context, content_title_text)


@when('根据title查询创建的cpl的uuid')
def query_content_by_title(context):
    content_action.query_content_by_str(context, context.content_title_text)


@when('content列表可以查询到刚创建的cpl')
def query_content_by_title(context):
    content_action.query_content_by_str(context, context.content_title_text)
    context.content_uuid_list = jsonpath.jsonpath(context.resp, '$..uuid')


"""
---------------------------------edit_placeholder_content---------------------------------
"""


@when(
    "修改属性{access_audio},'{access_subtitles}','{audio}','{content_kind}','{dimension}','{duration_numerator}','{edit_rate}','{facility}','{language}','{resolution}','{special_effect}','{studio}','{subtitles}','{visual_format}'的值时")
def edit_content_attr(context, access_audio, access_subtitles, audio, content_kind,
                      dimension, duration_numerator, edit_rate, facility, language, resolution, special_effect, studio,
                      subtitles, visual_format):
    cpl_uuid = context.content_uuid
    content_action.edit_content_attr(context, cpl_uuid, access_audio, access_subtitles, audio, content_kind, dimension,
                                     duration_numerator, edit_rate, facility, language, resolution, special_effect,
                                     studio, subtitles, visual_format)


@when('修改offset_time中的rolling_credit为1s到7200s随机')
def edit_offset_time_rolling_credit(context):
    content_action.edit_content_offset_time(context, cpl_uuid=context.content_uuid,
                                            modify_types='rolling_credit')


@when('修改offset_time中的credit_offset为1s到7200s随机')
def edit_offset_time_credit_offest(context):
    content_action.edit_content_offset_time(context, cpl_uuid=context.content_uuid,
                                            modify_types='credit_offset')


@when('修改offset_time中的hard_lock_offset为1s到7200s随机')
def edit_offset_time_hard_lock_offset(context):
    content_action.edit_content_offset_time(context, cpl_uuid=context.content_uuid,
                                            modify_types='hard_lock_offset')


@when('修改offset_time中的screenwriter_credit_offset为1s到7200s随机')
def edit_offset_time_screenwriter_credit_offset(context):
    content_action.edit_content_offset_time(context, cpl_uuid=context.content_uuid,
                                            modify_types='screenwriter_credit_offset')


"""
---------------------------------create_playlist---------------------------------
"""


@when('成功创建名字为变量{playlist}的playlist')
def create_successfur_playlist(context, playlist):
    playlist_actions.create_static_playlist(context, playlist)


@when('查询影院上传的场次属性show_attribute获取第一个参数')
def query_show_attribute(context):
    playlist_actions.query_show_attribute_in_creat_auto_playlist(context)


@when('输入pos_show_attributes,创建变量为{playlist}的auto_playlist')
def create_auto_playlist(context, playlist):
    playlist_actions.create_auto_playlist(context, playlist, context.pos_show_attributes_list)


"""
---------------------------------playlist_query_placeholder_content---------------------------------
"""


@when('根据playlist_uuid查找状态为draft的playlist的version和已存在的草稿信息')
def qurey_playlist_version(context):
    playlist_actions.query_playlist_version_uuid_and_other_detail(context, context.playlist_uuid)
    a = jsonpath.jsonpath(context.resp, '$...data.versions[?(@.status=="draft")]')
    logging.info('a' * 1000)
    logging.info(a)
    context.playlist_version_uuid = a[0]['playlist_version_uuid']
    context.show_attribute_groups = a[0]['show_attribute_groups']
    context.content_list = []
    if a[0]['content_list'] != []:
        for i in a[0]['content_list']:
            context.content_list.append(
                {'content_association_uuid': i['content_association_uuid'], 'content_id': i['content_id'],
                 'content_type': i['content_type'], 'extension': i['extension'], 'title': i['title']}
            )


@when('在library里查询content，并让content属性作为旧属性')
def qurey_content_in_library(context):
    playlist_actions.query_content_in_library(context, library_type='cpl', content_title=context.content_uuid)
    context.old_content_attr = context.resp.get('data')[0].get('extension')


@when('在library里查询content')
def qurey_content_in_library(context):
    playlist_actions.query_content_in_library(context, library_type='cpl', content_title=context.content_uuid)


@when('在library里查询segment')
def qurey_segment_in_library(context):
    playlist_actions.query_content_in_library(context, library_type='segment', content_title=context.segment_title)
    context.old_content_attr = context.resp.get('data')[0].get('extension')


@when('在library里查询macro')
def qurey_segment_in_library(context):
    playlist_actions.query_content_in_library(context, library_type='macro', content_title=context.macro_title)
    context.old_content_attr = context.resp.get('data')[0].get('extension')


@when('在library里查询automation')
def qurey_segment_in_library(context):
    playlist_actions.query_content_in_library(context, library_type='automation')
    context.automation_name = jsonpath.jsonpath(context.resp, '$..title')[0]


@when('把content加到playlist里并保存草稿')
def create_playlist_and_save_draft(context):
    def dict_to_json_str(source: dict):
        if not source:
            return
        return json.dumps(source)

    try:
        c = jsonpath.jsonpath(context.resp, '$...data[?(@.content_id=="%s")]' % context.content_uuid)
        dict_to_json_str(c[0]['extension'])
        context.content_list.extend(c)
        playlist_actions.add_draft_to_playlist(context, playlist_version=context.playlist_version_uuid,
                                               playlist_uuid=context.playlist_uuid,
                                               content_list=context.content_list,
                                               show_attribute_groups=context.show_attribute_groups)

    except:
        logging.info('请求出错')


@when('把segment加到playlist里并保存草稿')
def create_playlist_and_save_draft(context):
    def dict_to_json_str(source: dict):
        if not source:
            return
        return json.dumps(source)

    c = jsonpath.jsonpath(context.resp, '$...data[?(@.content_id=="%s")]' % context.segment_uuid)
    dict_to_json_str(c[0]['extension'])
    context.content_list.extend(c)
    playlist_actions.add_draft_to_playlist(context, playlist_version=context.playlist_version_uuid,
                                           playlist_uuid=context.playlist_uuid,
                                           content_list=context.content_list,
                                           show_attribute_groups=context.show_attribute_groups)


@when('把macro加到playlist里并保存草稿')
def create_playlist_and_save_draft(context):
    def dict_to_json_str(source: dict):
        if not source:
            return
        return json.dumps(source)

    try:
        c = jsonpath.jsonpath(context.resp, '$...data[?(@.content_id=="%s")]' % context.macro_uuid)
        dict_to_json_str(c[0]['extension'])
        context.content_list.extend(c)
        playlist_actions.add_draft_to_playlist(context, playlist_version=context.playlist_version_uuid,
                                               playlist_uuid=context.playlist_uuid,
                                               content_list=context.content_list,
                                               show_attribute_groups=context.show_attribute_groups)
    except:
        logging.info('请求出错')


@when('查询在playlist_detail返回的结果version.content_list.extension属性为新属性')
def query_playlist_detail(context):
    playlist_actions.query_playlist_version_uuid_and_other_detail(context, context.playlist_uuid)
    b = '$..?(@.content_id=="%s")' % context.content_uuid
    c = jsonpath.jsonpath(context.resp, b)
    context.new_content_attr = c[0]['extension']
    logging.info(f'新属性为{context.new_content_attr}')


"""
---------------------------------playlist_query_complex_content---------------------------------
"""


@when('查询影院上传的content的uuid')
def edit_complex_content_attr(context):
    content_action.query_complex_content(context)


"""
---------------------------------query_playlist---------------------------------
"""


@when('查看playlsit播放列表')
def query_playlist_list(context):
    playlist_actions.query_playlist_by_str(context, context.playlist_title)
    context.playlist_uuid_list = jsonpath.jsonpath(context.resp, '$..pplUuid')
    logging.info(f'查询的列表uuid{context.playlist_uuid_list}')


"""
---------------------------------publish_playlist---------------------------------
"""


@when('publish该playlist')
def publish_playlist(context):
    playlist_actions.publish_playlist(context, context.playlist_version_uuid)


"""
---------------------------------sagment---------------------------------
"""


@when('默认"split_by_week"为false时创建third_parth类型的segment时type={type}和purpose={purpose}和输入变量title为{title}时')
def create_segment(context, type, title, purpose):
    segment_action.creat_segment(context, type=type, title=title, purpose=purpose)


@when('默认"split_by_week"为false时创建playlist类型的segment时type={type}和purpose={purpose}和输入变量title为{title}时')
def create_segment(context, type, title, purpose):
    segment_action.creat_segment(context, type=type, title=title, purpose=purpose)


@when('默认"split_by_week"为false时创建title类型的segment时type={type}和purpose={purpose}和输入变量title为{title}时')
def create_segment(context, type, title, purpose):
    segment_action.creat_segment(context, type=type, title=title, purpose=purpose)


@when('默认"split_by_week"为false时创建org-segment类型的segment时type={type}和purpose={purpose}和输入变量title为{title}时')
def create_segment(context, type, title, purpose):
    segment_action.creat_segment(context, type=type, title=title, purpose=purpose)


@when('根据title列表中查询出的uuid列表')
def query_segment_uuid_list(context):
    segment_action.query_segment_by_str(context)


"""
---------------------------------marco---------------------------------
"""


@when('输入变量为{title}和type={type}时获取macro_uuid')
def create_macro(context, title, type):
    macro_action.create_macro(context, title, type)


@when('根据title列表中查询出的macro_uuid列表')
def query_macro_uuid_list(context):
    macro_action.query_macro_by_str(context)


"""
---------------------------------shows---------------------------------
"""


@when('查询全部shows获取pos_name_list，pos_one_name_list')
def query_all_shows(context):
    show_actions.query_shows_match_title(context)

@when('查询全部shows获取pos_name_list，pos_one_name_list用于match—title')
def query_all_shows1(context):
    show_actions.query_shows_match_title1(context)

@when('请求列表获取未锁定而且没有match_title获取show_title_name')
def qurey_unmatch_shows(context):
    show_actions.query_shows_match_title(context, states=['unassigned'], match_title_bool=False)


@when('请求列表获取未锁定而且有match_title获取show_title_name')
def query_match_shows(context):
    show_actions.query_shows_match_title(context, states=['unassigned'], match_title_bool=True)


@when('show页面接口查询有screen_show_attributes属性的pos同时提取show_title_name、pos_show_attributes属性和pos_uuid')
def query_no_assigned_have_show_attr(context):
    show_actions.query_no_assigned_have_show_attr(context)


@when('show页面接口查询有screen_show_attributes属性的pos同时提取show_title_name、pos_show_attributes属性和pos_uuid1')
def query_no_assigned_have_show_attr1(context):
    show_actions.query_no_assigned_have_show_attr1(context)


@when('show页面接口查询有screen_show_attributes属性的pos同时提取show_title_name、pos_show_attributes属性和pos_uuid2')
def query_no_assigned_have_show_attr2(context):
    show_actions.query_no_assigned_have_show_attr2(context)


@when('输入单个pos_one_name_list和title_uuid进行match_pos')
def match_no_title_show(context):
    show_actions.macth_title(context, show_name_list=context.pos_one_name_list, title_uuid=context.title_uuid)


@when('输入单个pos_name_list和title_uuid进行unmatch_pos')
def unmatch_show(context):
    show_actions.unmacth_title(context, show_name_list=context.pos_one_name_list, title_uuid=context.title_uuid)


@when('输入多个pos_name_list和title_uuid进行match_pos')
def match_no_title_show(context):
    show_actions.macth_title(context, show_name_list=context.pos_name_list, title_uuid=context.title_uuid)


@when('输入多个pos_name_list和title_uuid进行unmatch_pos')
def unmatch_no_title_show(context):
    show_actions.unmacth_title(context, show_name_list=context.pos_name_list, title_uuid=context.title_uuid)


@when('等待10s')
def wait_ten_second(context):
    logging.info('等待运行中......')
    time.sleep(10)


@when('等待5s')
def wait_ten_second(context):
    logging.info('等待运行中......')
    time.sleep(5)


@when('等待90s')
def wait_ten_second(context):
    logging.info('等待运行中......')
    time.sleep(120)


@when('关键字show_title_name查询列表，获取title_uuid_list')
def query_show_get_title_uuid_list(context):
    show_actions.query_shows_match_title(context, search_name=context.pos_one_name_str)
    context.show_title_uuid_list = jsonpath.jsonpath(context.resp, '$..title_uuid')
    if context.show_title_uuid_list == False:
        context.show_title_uuid_list = []


@when('根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于assigned')
def query_show_get_pos_uuid_and_pos_name_list_no_show_attr(context):
    show_actions.query_shows_get_pos_uuid(context)
    context.pos_one_name_str = context.all_show_name_pos_uuid_list[0]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = context.all_show_name_pos_uuid_list[0]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)


@when('根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于unassigned')
def query_show_get_pos_uuid_and_pos_name_list_no_show_attr(context):
    show_actions.query_shows_get_pos_uuid(context)
    context.pos_one_name_str = context.all_show_name_pos_uuid_list[1]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = context.all_show_name_pos_uuid_list[1]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)


@when('根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于query_assigned')
def query_show_get_pos_uuid_and_pos_name_list_no_show_attr(context):
    show_actions.query_shows_get_pos_uuid(context)
    context.pos_one_name_str = context.all_show_name_pos_uuid_list[2]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = context.all_show_name_pos_uuid_list[2]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)


@when('根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于query_unassigned')
def query_show_get_pos_uuid_and_pos_name_list_no_show_attr(context):
    show_actions.query_shows_get_pos_uuid(context)
    context.pos_one_name_str = context.all_show_name_pos_uuid_list[3]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = context.all_show_name_pos_uuid_list[3]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)

@when('根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于create_macro_and_add_standard_playlist')
def query_show_get_pos_uuid_and_pos_name_list_no_show_attr(context):
    show_actions.query_shows_get_pos_uuid(context)
    context.pos_one_name_str = context.all_show_name_pos_uuid_list[4]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = context.all_show_name_pos_uuid_list[4]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)

@when('根据show_title_name获取没有shows属性show的pos_uuid和pos_name_list用于create_title_segment_add_standard_playlist')
def query_show_get_pos_uuid_and_pos_name_list_no_show_attr(context):
    show_actions.query_shows_get_pos_uuid(context)
    context.pos_one_name_str = context.all_show_name_pos_uuid_list[5]['name']
    context.pos_one_name_list = []
    context.pos_one_name_list.append(context.pos_one_name_str)
    context.pos_uuid = context.all_show_name_pos_uuid_list[5]['pos_uuid']
    context.pos_uuid_list = []
    context.pos_uuid_list.append(context.pos_uuid)


@when('用playlist_uuid和pos_uuid去assigned场次')
def assigned_shows(context):
    show_actions.assigned_shows(context, playlist_uuid=context.playlist_uuid, pos_uuid_list=context.pos_uuid_list)


@when('对该pos_uuid进行unassigned')
def unassigned_show(context):
    show_actions.unassigned_shows(context, pos_uuid_list=context.pos_uuid_list)


@when('在show_detail页面查询上述执行情况')
def query_show_detail(context):
    try:
        for i in range(30):
            show_actions.qurey_show_detail(context, context.pos_uuid)
            if context.state == 'pending':
                i += 1
                time.sleep(20)
            else:
                break
        return context.resp
    except:
            with allure.step('此时状态'):
                allure.attach(name='状态:', body=str(context.state))

@when('在standard_playlist_manage_shows页面查询上述执行情况')
def query_standard_playlist_manage_shows(context):
    playlist_actions.query_playlist_manage_shows(context, playlist_uuid=context.playlist_uuid,
                                                 automatically_apply=False,
                                                 show_attribute=[])


@when('在auto_playlist_manage_shows页面查询上述执行情况')
def query_standard_playlist_manage_shows(context):
    playlist_actions.query_playlist_manage_shows(context, playlist_uuid=context.playlist_uuid, automatically_apply=True,
                                                 show_attribute=context.pos_show_attributes_list)


@when('在segment_manage_shows页面查询上述执行情况')
def query_standard_playlist_manage_shows(context):
    segment_action.query_segment_manage_shows(context, split_uuid=context.split_uuid,
                                              content_association_uuid=context.content_association_uuid,
                                              title_uuid=context.title_uuid)


@when('在process_queue页面查询上述执行情况')
def query_process_queues(context):
    playlist_actions.query_process_queues(context, name=context.playlist_title)


@when('在process_queue页面查询segment发布状态')
def query_process_queues(context):
    playlist_actions.query_process_queues(context, name=context.segment_title, sections=['segment'])


@when('在process_queue页面查询macro发布状态')
def query_process_queues(context):
    playlist_actions.query_process_queues(context, name=context.macro_title, sections=['macro'])


@when('在show_detail页面查询上述执行情况，如果匹配完成，获取content_association_uuid和action_tag_uuid')
def query_show_detail_get_content_association_uuid(context):
    try:

        for i in range(30):
            show_actions.qurey_show_detail(context, context.pos_uuid)
            if context.state == 'pending':
                i+=1
                time.sleep(20)
            else:
                break
        context.content_association_uuid = jsonpath.jsonpath(context.resp, '$..content_association_uuid')[0]
        context.action_tag_uuid = jsonpath.jsonpath(context.resp, '$..events[*][uuid]')[0]
        return context.resp
    except:
            with allure.step('此时状态可能未完成，请页面查看'):
                allure.attach(name='状态:', body=str(context.state))




@when('在show_detail页面查询上述执行情况，如果匹配完成，获取content_association_uuid和action_tag_uuid用于segment放在第二的位置')
def query_show_detail_get_content_association_uuid(context):
    try:
        for i in range(30):
            show_actions.qurey_show_detail(context, context.pos_uuid)
            if context.state == 'pending':
                i += 1
                time.sleep(20)
            else:
                break
        context.content_association_uuid = jsonpath.jsonpath(context.resp, '$..content_association_uuid')[1]
        context.action_tag_uuid = jsonpath.jsonpath(context.resp, '$..events[*][uuid]')[1]
        return context.resp
    except:
        with allure.step('此时状态可能未完成，请页面查看'):
            allure.attach(name='状态:', body=str(context.state))



@when('根据content_association_uuid和title_uuid查询segment的split_uuid')
def edit_segment(context):
    segment_action.query_segment_split_detail(context, content_association_uuid=context.content_association_uuid,
                                              title_uuid=context.title_uuid)
    context.split_uuid = jsonpath.jsonpath(context.resp, '$..segment_split_infos[*][uuid]')[0]


@when('根据content_association_uuid获取第一组macro的split_uuid')
def edit_segment(context):
    segment_action.query_macro_split_detail(context, content_association_uuid=context.macro_uuid)
    context.split_uuid = jsonpath.jsonpath(context.resp, '$..segment_split_infos[*][uuid]')[1]


@when('把content加到title_segment里保存草稿')
def create_title_segment_and_save_draft(context):
    def dict_to_json_str(source: dict):
        if not source:
            return
        return json.dumps(source)

    try:
        c = jsonpath.jsonpath(context.resp, '$...data[?(@.content_id=="%s")]' % context.content_uuid)
        dict_to_json_str(c[0]['extension'])
        logging.info(c)
        context.content_list = c
        segment_action.add_draft_in_segment(context)
    except:
        logging.info('请求出错')


@when('把automation加到Dynamic_macro里保存草稿')
def create_title_segment_and_save_draft(context):
    def dict_to_json_str(source: dict):
        if not source:
            return
        return json.dumps(source)

    try:
        c = jsonpath.jsonpath(context.resp, '$...data[0]')

        dict_to_json_str(c[0]['extension'])
        logging.info(c)
        context.content_list = c
        segment_action.add_draft_in_segment(context)
    except:
        logging.info('请求出错')


@when('publish该title_segment')
def publist_title_segment(context):
    segment_action.publish_title_segment(context)


@when('publish该Dynamic_macro')
def publist_title_segment(context):
    segment_action.publish_Dynamic_macro(context)
