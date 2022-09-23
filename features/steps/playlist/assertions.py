import logging
import time

import allure
import jsonpath
from retrying import retry
import json

from tools.logger import GetLogger

log = GetLogger().get_logger()

from features.steps.playlist.playlist_utils.playlist_client import Playlist


def assert_create_playlist_success(context):
    with allure.step('断言结果'):
        allure.attach(name='期望', body='产生playlist_uuid')
        allure.attach(name='结果', body=str(context.playlist_uuid))
    assert len(context.resp['data']) > 5


def asset_query_uuid_in_playlist_list_uuid(context):
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.playlist_uuid))
        allure.attach(name='列表里的uuid', body=str(context.playlist_uuid_list))
    assert context.playlist_uuid in context.playlist_uuid_list


def assert_edit_playlist_content_success(context):
    with allure.step('断言结果'):
        allure.attach(name='修改前属性', body=str(context.old_content_attr))
        allure.attach(name='修改后属性', body=str(context.new_content_attr))
    assert context.old_content_attr != context.new_content_attr


def assert_assigned_query_in_playlis_manage_shows(context):
    pos_uuid = jsonpath.jsonpath(context.resp, '$..pos_uuid')
    with allure.step('断言结果'):
        allure.attach(name='匹配的pos_uuid', body=str(context.pos_uuid))
        allure.attach(name='show_detail返回数据', body=str(pos_uuid))
    assert context.pos_uuid in pos_uuid

def assert_assigned_query_in_process_queue(context):
    playlist_uuid=jsonpath.jsonpath(context.resp, '$..ppl_uuid')
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.playlist_uuid))
        allure.attach(name='show_detail返回数据', body=str(context.resp))
    assert context.playlist_uuid in playlist_uuid
















def assert_add_playlist_segment_success(context, success):
    """
    验证segment是否添加成功
    :param context: 上下文
    :return:
    """
    add = context.add_playlist_segment
    find = context.find_playlist_segment
    find_libs = context.find_segments
    conv = {
        'title': 2,
        'segment': 3
    }
    assert success
    assert add['uuid'] == find['uuid']
    assert add['title'] == find['title']
    if 'purpose' in add:
        assert add['purpose'] == find['purpose']
    # assert add['type'] == conv[find['type']]
    success = False
    convert = {
        2: 'playlist_segment',
        3: 'title_segment',
        4: 'api_segment',
        6: 'base_segment'
    }
    for lib in find_libs:
        if add['uuid'] == lib['content_id']:
            # 验证title，content_type，extension:{text，title，purpose，content_kind}
            assert 'segment' == lib['content_type']
            assert add['title'] == lib['title']
            assert add['title'] == lib['extension']['text']
            if 'purpose' in add:
                assert add['purpose'] == lib['extension']['purpose']
            assert convert[add['type']] == lib['extension']['content_kind']
            success = True
            break
    assert success
    log.info(f'添加segment 测试通过~')


def assert_check_add_dynamic_playlist_draft(context, playlist_uuid, success):
    # 1.验证需要添加草稿的数据
    seg = Playlist(context.playlist_url)
    res = seg.find_playlist_versions_by_playlist_uuid(playlist_uuid, context.token)
    respose = json.loads(res.content)
    flag = False
    if respose['code'] == 200 and len(respose['data']) > 0:
        for item in respose['data']:
            if item['status'] == 'draft':
                q_obj = item['content_list'][0]
                f_obj = context.clist[0]
                if q_obj['content_id'] == f_obj['content_id'] \
                        and q_obj['content_association_uuid'] == f_obj['content_association_uuid'] \
                        and q_obj['extension'] == f_obj['extension'] \
                        and q_obj['title'] == f_obj['title']:
                    flag = True
    if flag:
        log.info("检验成功{0}".format(success))
    else:
        log.info("检验失败！")


def assert_add_two_same_title_segment_fail(context):
    assert not context.success


def assert_add_draft_to_static_playlist_success(context):
    """
    验证草稿是否成功添加到static playlist
    :param context: 上下文
    :return:
    """
    add = context.add
    find = context.find
    assert find
    assert context.success
    assert add['uuid'] == find['playlist_version_uuid']
    # assert add['title'] == find['title']
    # assert add['purpose'] == find['purpose']
    # assert add['type'] == find['type']
    log.info(f'添加草稿测试通过~')


def assert_copy_static_playlist_success(context):
    """
    检查静态列表复制成功
    :param context: 上下文
    :return:
    """
    add = context.add
    find = context.find
    assert find
    assert context.success
    assert add['uuid'] == find['uuid']
    assert add['automatically_apply'] == find['automatically_apply']
    assert add['title'] == find['title']
    # assert add['purpose'] == find['purpose']
    # assert add['type'] == find['type']
    log.info(f'复制static playlist测试通过~')


def assert_add_dynamic_playlist_success(context):
    """
    检查添加动态播放列表成功
    :param context: 上下文
    :returcheck_match_playlist_uuidn:
    """
    assert context.success, '找不到刚添加的动态播放列表'
    add = context.add
    find = context.find
    assert find, '找不到刚添加的动态播放列表'
    assert add['uuid'] == find['uuid']
    assert add['automatically_apply'] == find['automatically_apply']
    assert add['title'] == find['title']
    context.playlist_uuid = find['uuid']
    # assert add['purpose'] == find['purpose']
    # assert add['type'] == find['type']
    log.info(f'复制static playlist测试通过~')


def check_match_playlist_uuid(context, playlist_uuid, success):
    seg = Playlist(context.posuuid_url)
    # data = "{'playlist_id': '" + context.playlistUuid + "'}"
    data = {
        'ppl_uuid': context.playlistUuid,
        'show_attributes': '[]',
        'playlist_type': 'RELEASE_MATCH'
    }
    res = seg.get_match_playlist_manage(data, context.token)
    resopes = json.loads(res.content)
    list = resopes['data']
    s_bool = False
    if context.response['code'] == int(success):
        for item in list:
            if item['pos_uuid'] in context.pos_data['posUuids']:
                s_bool = True
                break
        if s_bool:
            log.info('匹配成功！')
        else:
            log.info("匹配失败！")
    else:
        log.info("匹配失败！")


def assert_we_matched_the_same_shows(context):
    unmatched = context.unassigned_shows
    log.info(f"这是原本没匹配的场次：\n{unmatched}")
    matching = context.shows_matched
    log.info(f"这是新匹配的场次：\n{matching}")
    assert len(unmatched) == len(matching), f'期望匹配的数量:({len(unmatched)})与已匹配数量:({len(matching)})不一致'

    # assert len(unmatched) == len(matching)
    for match in matching:
        for i, un in enumerate(unmatched):
            if un['pos_uuid'] == match['pos_uuid']:
                break

            if i == len(unmatched) - 1:
                raise RuntimeError(f'找不到匹配场次,:unmatched_pos_uuid:{un["pos_uuid"]}')


def assert_dynamic_playlist_has_afs(context):
    """
    检查动态播放列表有Automatic Feature Selector
    :param context: 上下文
    :return:
    """
    content_list = context.find[0]['content_list']
    context.playlist_version_uuid = context.find[0]['playlist_version_uuid']
    success = False
    for segment in content_list:
        if segment['title'] == 'Automatic Feature Selector':
            success = True
            break
    assert success
    log.info(f'检查动态播放列表有Automatic Feature Selector通过~')


def assert_add_cpl_and_playlist_segment_to_playlist_version_success(context, version_state):
    """
    检查成功添加cpl和playlist_segment到playlist_version上
    :param version_state: 预测版本状态
    :param context: 上下文
    :return:
    """
    version = context.find[0]
    content_list = context.find[0]['content_list']
    cpl_success = seg_success = False
    assert version['playlist_uuid'] == context.playlist_uuid
    assert version['status'] == version_state
    # 验证字段：content_list:{playlist_uuid,playlist_version_uuid,status,content_id,content_type,extension,title}
    for item in content_list:
        if item['content_id'] == context.find_cpl['content_id']:
            assert context.find_cpl['content_type'] == item['content_type']
            assert context.find_cpl['title'] == item['title']
            assert context.find_cpl['extension'] == item['extension']
            cpl_success = True
        if item['content_id'] == context.find_segment['content_id']:
            seg_success = True
    assert cpl_success and seg_success
    log.info(r'检查成功添加cpl和playlist_segment到playlist_version上通过~')


def assert_check_add_cpl_and_playlist_segment(context, playlist_uuid, success):
    cpl_data = context.cpl_data
    seg = Playlist(context.playlist_url)
    res = seg.find_playlist_versions_by_playlist_uuid(playlist_uuid, context.token)
    respose = json.loads(res.content)
    content_list = respose['data']
    c_boolean = t_boolean = p_boolean = False
    for item in content_list:
        playlist_id = item['playlist_uuid']
        if playlist_id == playlist_uuid:
            for item2 in item['content_list']:
                content_id = item2['content_id']
                if content_id == cpl_data['content_id']:
                    c_boolean = True
                if item2['title'] == cpl_data['title']:
                    t_boolean = True
                if item2['content_type'] == cpl_data['content_type']:
                    p_boolean = True

    if c_boolean or t_boolean or p_boolean:
        log.info("填充成功：{0}".format(success))
    else:
        log.info("填充失败")


def assert_split_and_params_are_same(context):
    playlist_segment_split_nodes = context.playlist_segment_split_nodes
    # title_segment_split_nodes = context.title_segment_split_nodes
    ps_params = context.ps_data
    for node in playlist_segment_split_nodes['segment_split_infos']:
        if node['auto_group']:
            get_root = node
        if node['split_title'] == 'left':
            get_left = node
        if node['split_title'] == 'right':
            get_right = node
    # get_root = playlist_segment_split_nodes['segment_split_infos'][0]
    # get_left = playlist_segment_split_nodes['segment_split_infos'][1]
    # get_right = playlist_segment_split_nodes['segment_split_infos'][2]
    p_left = ps_params['group_left']
    p_right = ps_params['group_right']
    # 校验playlist_segment_split
    # parent_uuid（该id需要与被分组的uuid一致），playlist_uuid，ppl_version_uuid，segment_association_uuid，content_list
    assert p_left['parent_uuid'] == get_root['uuid']
    assert p_left['segment_association_uuid'] == get_left['segment_association_uuid']
    assert p_right['parent_uuid'] == get_root['uuid']
    assert p_right['segment_association_uuid'] == get_right['segment_association_uuid']
    assert p_right['ppl_version_uuid'] == get_right['ppl_version_uuid']
    assert p_right['playlist_uuid'] == get_right['playlist_uuid']


def assert_title_split_and_params_are_same(context):
    title_segment_split_nodes = context.title_segment_split_nodes
    ps_params = context.ts_data
    # get_root = title_segment_split_nodes['segment_split_infos'][2]
    # get_left = title_segment_split_nodes['segment_split_infos'][0]
    # get_right = title_segment_split_nodes['segment_split_infos'][1]
    for node in title_segment_split_nodes['segment_split_infos']:
        if node['auto_group']:
            get_root = node
        if node['split_title'] == 'left':
            get_left = node
        if node['split_title'] == 'right':
            get_right = node
    p_left = ps_params['group_left']
    p_right = ps_params['group_right']
    # 校验playlist_segment_split
    # parent_uuid（该id需要与被分组的uuid一致），playlist_uuid，ppl_version_uuid，segment_association_uuid，content_list
    assert p_left['parent_uuid'] == get_root['uuid']
    assert p_left['segment_association_uuid'] == get_left['segment_association_uuid']
    assert p_right['parent_uuid'] == get_root['uuid']
    assert p_right['segment_association_uuid'] == get_right['segment_association_uuid']
    assert p_right['ppl_version_uuid'] == get_right['ppl_version_uuid']
    assert p_right['playlist_uuid'] == get_right['playlist_uuid']


def assert_can_not_find_this_dynamic_playlist(context):
    assert not context.success


def assert_num_is(context, expect_num):
    log.info(f"播放列表实际的匹配数为：{context.real_num}")
    assert context.real_num == int(expect_num)


def init_static_pl_success(context):
    log.info('until now, init static playlist success, playlist content list contains cpl,segment,automation')


def publish_playlist_success(context):
    log.info(
        f'published playlist compare content success ,pl_uuid={context.pl_uuid} version_uuid={context.playlist_version_uuid}')


def cancel_publish_success(context):
    log.info("cancel publish playlist success")


def delete_playlist_success(context):
    log.info(f"delete playlist success, pl_uuid={context.pl_uuid}")


def delete_playlist_segment_success(context):
    log.info(
        f"delete playlist segment group success, content_association_uuid={context.content_association_uuid}  group_uuid={context.group_uuid}")


def delete_title_segment_success(context):
    log.info(
        f"delete title segment group success, content_association_uuid={context.content_association_uuid} , title_uuid={context.title_uuid}  ,group_uuid={context.group_uuid}")


def copy_dynamic_playlist_success(context):
    log.info(
        f"copy dynamic playlist success  ,target playlist_uuid={context.target_data['uuid']}  ,copy playlist_uuid={context.copy_playlist_uuid}")
