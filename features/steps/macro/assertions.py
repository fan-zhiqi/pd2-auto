import allure
import jsonpath


def assert_create_macro_success(context):
    with allure.step('断言结果'):
        allure.attach(name='期望', body='产生macro_uuid')
        allure.attach(name='结果', body=str(context.macro_uuid))
    assert len(context.resp['data']) > 5

def asset_query_uuid_in_macro_list_uuid(context):
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.macro_uuid))
        allure.attach(name='列表里的uuid', body=str(context.macro_uuid_list))
    assert context.macro_uuid in context.macro_uuid_list


def assert_query_publist_macro_in_process_queue(context):
    macro_uuid = jsonpath.jsonpath(context.resp, '$..uuid')
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.macro_uuid))
        allure.attach(name='show_detail返回数据', body=str(context.resp))
    assert context.macro_uuid in macro_uuid

def assert_query_automation_title_in_show_detail(context):
    title = jsonpath.jsonpath(context.resp, '$..events[*][name]')
    with allure.step('断言结果'):
        allure.attach(name='创建的content的标题', body=str(context.automation_name))
        allure.attach(name='show_detail返回数据', body=str(context.resp))
    assert context.automation_name in title