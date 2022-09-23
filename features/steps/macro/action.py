import json
import logging
import random

import jsonpath

from features.steps.macro.macro_util.macro_client import MacroClient


def create_macro(context, title, type):
    context.macro_title = title + str(random.randint(1, 1111111111111))
    data = {"title": context.macro_title, 'content_kind': type}
    res = MacroClient(context.playlist_url).create_macro(context.token, data=data)
    context.resp = res.json()
    context.macro_uuid = context.resp['data']
    return context.resp


def query_macro_by_str(context):
    res = MacroClient(context.playlist_url).query_macro_by_title(context.token, context.macro_title)
    context.resp = res.json()
    context.macro_uuid_list = jsonpath.jsonpath(context.resp, '$..uuid')

    return context.resp
