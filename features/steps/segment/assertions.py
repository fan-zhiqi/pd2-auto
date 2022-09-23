import allure
import jsonpath


def assert_create_segment_success(context):
    with allure.step('断言结果'):
        allure.attach(name='期望', body='产生segment_uuid')
        allure.attach(name='结果', body=str(context.segment_uuid))
    assert len(context.resp['data']) > 5


def asset_query_uuid_in_segment_list_uuid(context):
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.segment_uuid))
        allure.attach(name='列表里的uuid', body=str(context.segment_uuid_list))
    assert context.segment_uuid in context.segment_uuid_list


def assert_create_content_title_in_show_detail(context):
    title = jsonpath.jsonpath(context.resp, '$..events[*][content_title_text]')
    with allure.step('断言结果'):
        allure.attach(name='创建的content的标题', body=str(context.content_title_text))
        allure.attach(name='show_detail返回数据', body=str(context.resp))
    assert context.content_title_text in title


def assert_assigned_query_in_segment_manage_shows(context):
    pos_uuid = jsonpath.jsonpath(context.resp, '$..pos_uuid')
    with allure.step('断言结果'):
        allure.attach(name='匹配的pos_uuid', body=str(context.pos_uuid))
        allure.attach(name='show_detail返回数据', body=str(pos_uuid))
    assert context.pos_uuid in pos_uuid


def assert_query_publist_segment_in_process_queue(context):
    segment_uuid = jsonpath.jsonpath(context.resp, '$...segment[uuid]')
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.segment_uuid))
        allure.attach(name='show_detail返回数据', body=str(context.resp))
    assert context.segment_uuid in segment_uuid
