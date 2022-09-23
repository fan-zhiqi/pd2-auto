#!/usr/bin/python
# -*-coding:utf-8 -*-
import datetime

import allure
import jsonpath


def assert_match_title_success(context, message):
    context.message = context.resp.get('message')
    with allure.step('断言结果'):
        allure.attach(name='期望结果', body=str(message))
        allure.attach(name='实际结果', body=str(context.message))
    assert context.message == message


def assert_create_uuid_query_in_title_uuid_list(context):
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.title_uuid))
        allure.attach(name='show列表里的uuid', body=str(context.show_title_uuid_list))
    assert context.title_uuid in context.show_title_uuid_list


def assert_create_uuid_query_not_in_title_uuid_list(context):
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.title_uuid))
        allure.attach(name='show列表里的uuid', body=str(context.show_title_uuid_list))
    assert context.title_uuid not in context.show_title_uuid_list


def assert_create_uuid_in_show_detail(context):
    ppl_uuid = jsonpath.jsonpath(context.resp, '$..ppl_uuid')
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.playlist_uuid))
        allure.attach(name='show_detail返回数据', body=str(context.resp))
    assert context.playlist_uuid in ppl_uuid

def assert_create_macro_uuid_in_show_detail(context):
    macro_uuid = jsonpath.jsonpath(context.resp, '$..uuid')
    with allure.step('断言结果'):
        allure.attach(name='创建的uuid', body=str(context.macro_uuid))
        allure.attach(name='show_detail返回数据', body=str(context.resp))
    assert context.macro_uuid in macro_uuid

def assert_query_show_detail_ppl_uuid_isNone(context):
    with allure.step('断言结果'):
        allure.attach(name='请求的响应数据', body=str(context.resp))
        allure.attach(name='show_detail返回的ppl_uuid', body=str(jsonpath.jsonpath(context.resp, '$..ppl_uuid')))
    assert jsonpath.jsonpath(context.resp, '$..ppl_uuid') == [None]

def assert_get_pos_message(context):
    with allure.step('断言结果'):
        allure.attach(name='pos_one_name_list', body=str(context.pos_one_name_list))
        allure.attach(name='pos_one_name_str', body=str(context.pos_one_name_str))
        allure.attach(name='pos_show_attributes_list',body=str(context.pos_show_attributes_list))
        allure.attach(name='获取的所有数据',body=str(context.a))

def assert_get_content_list(context):
    with allure.step('断言结果'):
        allure.attach(name='content_list', body=str(context.content_list))

def assert_get_action_tag_uuid(context):
    with allure.step('断言结果'):
        allure.attach(name='content_association_uuid', body=str(context.content_association_uuid))
        allure.attach(name='action_tag_uuid', body=str(context.action_tag_uuid))


def assert_get_pos_name(context):
    with allure.step('断言结果'):
        allure.attach(name='pos_name_list', body=str(context.pos_name_list))
        allure.attach(name='pos_one_name_list', body=str(context.pos_one_name_list))





def assert_receive_pos_week_raw(context, topic_name):
    '''
    验证pos-week.raw消息队列
    :param context: 上下文
    :param topic_name:
    :return:
    '''
    message = eval(context.kafka_consumer.get(topic_name=topic_name))
    current_week_number = message['data']['current_week_number']
    complex_uuid = message['data']['complex_uuid']
    current_year = datetime.datetime.now().isocalendar()
    current_week = current_year[1]

    assert current_week == current_week_number
    assert context.complex_uuid == complex_uuid


def assert_receive_pos_hash_raw(context, topic_name):
    '''
    验证pos-hash.raw消息队列
    :param context: 上下文
    :param topic_name:
    :return:
    '''
    message = eval(context.kafka_consumer.get(topic_name=topic_name))
    pos_map = message["data"]["pos_map"]
    complex_uuid = message["data"]["complex_uuid"]
    for k, v in list(pos_map.items())[0:1]:
        pos_map_key = k

    assert context.current_week == pos_map_key
    assert context.complex_uuid == complex_uuid


def assert_receive_pos_raw(context, topic_name):
    '''
    验证pos.raw消息队列消费
    :param context: 上下文
    :param topic_name:
    :return:
    '''

    message = eval(context.kafka_consumer.get(topic_name=topic_name))
    complex_uuid = message["data"]["complex_uuid"]

    assert context.complex_uuid == complex_uuid


def assert_receive_pos_mapping_response(context, topic_name):
    '''
    验证pos.mapping.response消息队列
    :param context: 上下文
    :param topic_name:
    :return:
    '''
    message = eval(context.kafka_consumer.get(topic_name=topic_name))
    pos_uuid = message["data"]["pos_uuid"]
    playlist_uuid = message["data"]["playlist_uuid"]
    complex_uuid = message["data"]["complex_uuid"]

    assert context.pos_uuid == pos_uuid
    assert context.playlist_uuid == playlist_uuid
    assert context.complex_uuid == complex_uuid


def assert_receive_cpl_locations_response(context, topic_name):
    '''
    验证cpl.locations.response消息队列
    :param context: 上下文
    :param topic_name:
    :return:
    '''
    message = eval(context.kafka_consumer.get(topic_name=topic_name))
    complex_uuid = message["data"]["complex_uuid"]

    assert context.complex_uuid == complex_uuid


def assert_receive_cpl_xml_response(context, topic_name):
    '''
    验证cpl.xml.response消息队列
    :param context: 上下文
    :param topic_name:
    :return:
    '''

    message = eval(context.kafka_consumer.get(topic_name=topic_name))
    complex_uuid = message["data"]["complex_uuid"]
    cpl_uuid = message["data"]["cpl_uuid"]

    assert context.complex_uuid == complex_uuid
    assert context.cpl_uuid == cpl_uuid

