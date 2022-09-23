import json
import random

import jsonpath

from features.steps.segment.segment_uitls.segment_client import SegmentClient


def creat_segment(context, type, title, purpose=''):
    '''ruc'''
    context.segment_title = title + str(random.randint(1, 1111111111111))
    data = {"type": type, "title": context.segment_title, "purpose": purpose, "split_by_week": False}

    res = SegmentClient(context.playlist_url).create_segment(context.token, data=data)
    context.resp = res.json()
    context.segment_uuid = context.resp['data']

    return context.resp


def query_segment_by_str(context):
    res = SegmentClient(context.playlist_url).query_segment_by_title(context.token, context.segment_title)
    context.resp = res.json()
    context.segment_uuid_list = jsonpath.jsonpath(context.resp, '$..uuid')
    return context.resp


def query_segment_split_detail(context, content_association_uuid, title_uuid=''):
    res = SegmentClient(context.playlist_url).query_segment_split_detail(context.token,
                                                                         content_association_uuid=content_association_uuid,
                                                                         title_uuid=title_uuid)
    context.resp = res.json()
    return context.resp

def query_macro_split_detail(context, content_association_uuid):
    res = SegmentClient(context.playlist_url).query_segment_split_detail(context.token,
                                                                         content_association_uuid=content_association_uuid
                                                                        )
    context.resp = res.json()
    return context.resp

def add_draft_in_segment(context):
    data = [{
        'split_uuid': context.split_uuid,
        'content_list': context.content_list,
        'ignored': False
    }]
    res = SegmentClient(context.playlist_url).add_draft_to_title_segment(context.token, data=data)


def publish_title_segment(context):
    res = SegmentClient(context.playlist_url).publish_title_segment(context.token, title_uuid=context.title_uuid,
                                                                    content_association_uuid=context.content_association_uuid,
                                                                    action_tag_uuid=context.action_tag_uuid)
def publish_Dynamic_macro(context):
    res = SegmentClient(context.playlist_url).publish_title_segment(context.token,
                                                                    content_association_uuid=context.action_tag_uuid,
                                                                    action_tag_uuid=context.action_tag_uuid)



def query_segment_manage_shows(context, split_uuid, content_association_uuid, title_uuid):
    res = SegmentClient(context.producer_view_url).query_segment_manage_shows(context.token, split_uuid,
                                                                              content_association_uuid,
                                                                              title_uuid=title_uuid)
    context.resp = res.json()
    return context.resp
