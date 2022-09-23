#!/usr/bin/python
# -*-coding:utf-8 -*-

from behave import then, given

import features.steps.api.assertions as api_assert
import features.steps.s3.assertions as s3_assert
import features.steps.title.assertions as title_assert
import features.steps.content.assertions as content_assert
import features.steps.playlist.assertions as playlist_assert
import features.steps.segment.assertions as segment_assert
import features.steps.macro.assertions as macro_assert
import features.steps.shows.assertions as shows_assert



@given('"{actor}" can access buckets "{bucket_name}" in s3')
@then('"{actor}" can access buckets "{bucket_name}" in s3')
def check_actor_can_access_buckets(context, actor, bucket_name):
    s3_assert.assert_actor_can_access_buckets(context, actor, bucket_name)


@then('"{actor}" can see "{file}" files in s3 bucket "{bucket_name}"')
def check_file_exists_in_s3_bucket(context, actor, file, bucket_name):
    s3_assert.assert_total_number_of_files_in_s3_bucket(
        context, actor, int(file), bucket_name
    )


@then('"{actor}" checks kdm is present in Unassigned '
      'Devices API with info "{dnqualifier}", "{recipient_name}", "{status}", '
      '"{total_kdms}"')
def check_kdm_present_in_unassigned_devices_api(
        context, actor, dnqualifier, recipient_name,
        status, total_kdms):
    api_assert.assert_kdm_available_on_unassigned_device_api(
        context, actor, dnqualifier, recipient_name,
        status, int(total_kdms)
    )


@then('"{actor}" checks that "{total_kdms}", '
      '"{total_devices}" has successfully been assigned to "{alias_name}"')
def check_kdm_present_in_assigned_devices_api(
        context, actor, total_kdms, total_devices, alias_name):
    api_assert.assert_kdm_available_on_assigned_device_api(
        context, actor, int(total_kdms),
        int(total_devices), alias_name
    )


"""
---------------------------------title--------------------------------------
"""


@then('请求成功断言data长度>5')
def assert_succesful_create_titels_case(context):
    title_assert.assert_successful_create_title(context)


@then('请求失败断言code=500')
def assert_fail_create_title_case(context):
    title_assert.assert_create_lack_name_title(context)


@then('断言message={message}')
def assert_repeat_creat_title_case(context, message):
    title_assert.assert_create_repeat_title(context, message)


@then('断言create创建的title_uuid在查询title_uuid的列表里面')
def assert_succesful_qurey_title_(context):
    title_assert.assert_create_title_in_query_title_list(context)




"""
---------------------------------content---------------------------------
"""


@then('断言code={code}')
def assert_succesful_message(context, code):
    content_assert.assert_successful_create_content(context, code)


@then('断言返回的message={message}')
def assert_repeat_name_content(context, message):
    content_assert.assert_message_success(context, message)


@then('创建的content在content列表中')
def assert_create_content_uuid_in_list(context):
    content_assert.assert_query_content(context)


@then('对比content旧属性')
def assert_content_attr_in_playlist(context):
    playlist_assert.assert_edit_playlist_content_success(context)


"""
---------------------------------playlist--------------------------------------
"""


@then('断言创建的playlist_uuid在播放列表里')
def assert_create_playlist_in_playlist_list(context):
    playlist_assert.asset_query_uuid_in_playlist_list_uuid(context)


@then('请求成功断言playlist_uuid长度>5')
def assert_succesful_create_playlist(context):
    playlist_assert.assert_create_playlist_success(context)


"""
---------------------------------segment--------------------------------------
"""


@then('请求成功断言segment_uuid长度>5')
def assert_create_segment(context):
    segment_assert.assert_create_segment_success(context)


@then('创建的uuid在列表中查询的uuid列表中')
def assert_query_segment_success(context):
    segment_assert.asset_query_uuid_in_segment_list_uuid(context)


"""
---------------------------------segment--------------------------------------
"""


@then('请求成功断言macro_uuid长度>5')
def assert_create_macro(context):
    macro_assert.assert_create_macro_success(context)


@then('创建的uuid在列表中查询的macro_uuid列表中')
def assert_query_macro_success(context):
    macro_assert.asset_query_uuid_in_macro_list_uuid(context)


"""
---------------------------------show--------------------------------------
"""

@then('创建的title_uuid在列表查询的title_uuid_list，match成功')
def assert_match_success(context):
    shows_assert.assert_create_uuid_query_in_title_uuid_list(context)


@then('创建的title_uuid不在列表查询的title_uuid_list，unmatch成功')
def assert_unmatch_success(context):
    shows_assert.assert_create_uuid_query_not_in_title_uuid_list(context)


@then('创建的playlist_uuid在show_detail页面里面')
def assert_assigned_sucess(context):
    shows_assert.assert_create_uuid_in_show_detail(context)

@then('创建的macro_uuid在show_detail页面里面')
def assert_assigned_sucess(context):
    shows_assert.assert_create_macro_uuid_in_show_detail(context)

@then('segment添加的content_title在show_detail页面里面')
def assert_assigned_sucess(context):
    segment_assert.assert_create_content_title_in_show_detail(context)

@then('macro添加的automation在show_detail页面里面')
def assert_assigned_sucess(context):
    macro_assert.assert_query_automation_title_in_show_detail(context)


@then('show_detail里的ppl为空')
def assert_assigned_sucess_in_show_detail(context):
    shows_assert.assert_query_show_detail_ppl_uuid_isNone(context)

@then('playlist_manage_shows页面里显示刚匹配的pos_uuid')
def assert_assigned_sucess_in_playlist(context):
    playlist_assert.assert_assigned_query_in_playlis_manage_shows(context)

@then('segment_manage_shows页面里显示刚匹配的pos_uuid')
def assert_assigned_sucess_in_playlist(context):
    segment_assert.assert_assigned_query_in_segment_manage_shows(context)

@then('process_queue页面显示该playlist_uuid')
def assert_assigned_suceess_in_process_queue(context):
    playlist_assert.assert_assigned_query_in_process_queue(context)

@then('process_queue页面显示该macro并且显示action为publish')
def assert_assigned_suceess_in_process_queue(context):
    macro_assert.assert_query_publist_macro_in_process_queue(context)

@then('process_queue页面显示该segment并且显示action为publish')
def assert_assigned_suceess_in_process_queue(context):
    segment_assert.assert_query_publist_segment_in_process_queue(context)


@then('成功获取参数pos_one_name_list和pos_one_name_str,pos_show_attributes')
def assert_get_pos_message(context):
    shows_assert.assert_get_pos_message(context)

@then('请求的content_list')
def assert_get_content_list(context):
    shows_assert.assert_get_content_list(context)

@then('获取的content_association_uuid和action_tag_uuid')
def assert_get_action_tag_uuid_and_content_association_uuid(context):
   shows_assert.assert_get_action_tag_uuid(context)


@then('查询的pos_name_list，pos_one_name_list的值')
def assert_get_pos(context):
    shows_assert.assert_get_pos_name(context)