#!/usr/bin/python
#-*-coding:utf-8 -*-
import json

import allure


def assert_successful_create_title(context):
    context.title_uuid = context.resp.get('data')
    with allure.step('断言结果'):
        allure.attach(name='期望结果', body='data数据长度大于5')
        allure.attach(name='实际结果', body=str(context.title_uuid))
    assert len(context.title_uuid) > 5

def assert_create_repeat_title(context,message):
    context.message = context.resp.get('message')
    with allure.step('断言结果'):
        allure.attach(name='期望结果', body=str(message))
        allure.attach(name='实际结果', body=str(context.message))
    assert context.message == message

def assert_create_lack_name_title(context,code):
    context.code = context.resp.get('code')
    with allure.step('断言结果'):
        allure.attach(name='期望结果', body=str(code))
        allure.attach(name='实际结果', body=str(context.code))
    assert context.code >= 500

def assert_create_title_in_query_title_list(context):
    with allure.step('断言结果'):
        allure.attach(name='期望结果', body=str(context.title_uuid))
        allure.attach(name='实际结果', body=str(context.title_uuid_list))
    assert context.title_uuid in context.title_uuid_list


def assert_title_list(context, has_result, params):
    has_result = True if has_result == 'True' else False
    title_list = context.title_list
    if has_result:
        assert len(title_list) > 0, f'断言查询有结果，但实际没有'
    else:
        assert len(title_list) == 0, f'断言查询无结果，但出现了{len(title_list)}条'

    res = json.loads(params)
    name = res['search']
    for item in title_list:
        if context.fuzzy:
            assert str.find(item['name'], name) > -1, f'title名称模糊不匹配，search:{name}, name: {item["name"]}'
        else:
            assert name == item['name'], f'title名称不匹配，search:{name}, name: {item["name"]}'


def assert_title_list_sort(context):
    asc = context.asc_title_list
    desc = context.desc_title_list
    assert len(asc) == len(desc), '升序与倒序列表长度不一样'
    desc = reversed(desc)
    for i, desc_item in enumerate(desc):
        if desc_item['uuid'] != asc[i]['uuid']:
            raise RuntimeError(f"发现第{i}个升序与倒序title列表元素不一样:{desc_item['uuid']}, {asc[i]['uuid']}")
