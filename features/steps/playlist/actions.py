import json
import random
from tools.logger import GetLogger

log = GetLogger().get_logger()

from features.steps.playlist.playlist_utils.playlist_client import Playlist


def create_static_playlist(context, title):
    random_title = title + str(random.randint(1300000000, 14000000000))
    context.playlist_title = random_title
    res = Playlist(context.playlist_url).create_static_playlist(context.token, context.playlist_title)
    context.resp = res.json()
    context.playlist_uuid = context.resp.get('data')
    return context.resp


def query_content_in_library(context, library_type: str, content_title=''):
    if library_type == 'cpl':
        res = Playlist(context.producer_view_url).query_content_in_library(context.token, library_type='cpl',
                                                                           search_title=content_title)
    elif library_type == 'segment':
        res = Playlist(context.producer_view_url).query_content_in_library(context.token, library_type='segment',
                                                                           search_title=content_title)
    elif library_type == 'pattern':
        res = Playlist(context.producer_view_url).query_content_in_library(context.token, library_type='pattern',
                                                                           search_title=content_title)
    elif library_type == 'macro':
        res = Playlist(context.producer_view_url).query_content_in_library(context.token, library_type='macro',
                                                                           search_title=content_title)
    elif library_type == 'automation':
        res = Playlist(context.producer_view_url).query_content_in_library(context.token, library_type='automation',
                                                                           device_type="emulator", device_model='T1000')
    else:
        res = Playlist(context.producer_view_url).query_content_in_library(context.token, library_type='cpl',
                                                                           search_title=content_title)
    context.resp = res.json()
    return context.resp


def query_playlist_version_uuid_and_other_detail(context, playlist_uuid):
    res = Playlist(context.playlist_url).query_playlist_version_uuid_and_other_detail(context.token, playlist_uuid)
    context.resp = res.json()
    return context.resp


def add_draft_to_playlist(context, playlist_version, content_list, playlist_uuid, show_attribute_groups=[]):
    '''该请求无响应内容'''
    data = {'playlist_uuid': playlist_uuid,
            'content_list': content_list,
            'show_attribute_groups': show_attribute_groups
            }
    res = Playlist(context.playlist_url).add_draft_to_playlist(context.token, data=data,
                                                               playlist_version=playlist_version)


def query_playlist_by_str(context, playlist_title: str):
    res = Playlist(context.playlist_url).query_playlist_by_title(context.token, playlist_title)
    context.resp = res.json()
    return context.resp


def query_show_attribute_in_creat_auto_playlist(context):
    res = Playlist(context.site_url).query_show_attribute(context.token)
    context.resp = res.json()
    context.pos_show_attributes_list = context.resp.get('data')
    return context.resp


def create_auto_playlist(context, playlist_title, attr=[]):
    context.playlist_title = playlist_title + str(random.randint(1, 1234456578))
    attribute_name = 'attr' + str(random.randint(1, 1234456578))
    res = Playlist(context.playlist_url).create_auto_playlist(context.token, attribute_name=attribute_name,
                                                              attrbute=attr, playlist_title=context.playlist_title)
    context.resp = res.json()

    context.playlist_uuid = context.resp.get('data')
    return context.resp


def publish_playlist(context, playlist_version_uuid):
    data = {"publish_later": False, "publish_time": None, "time_zone": "local"}
    res = Playlist(context.playlist_url).publish(context.token, data=data, playlist_version=playlist_version_uuid)


def query_playlist_manage_shows(context, playlist_uuid, automatically_apply, show_attribute):
    res = Playlist(context.producer_view_url).query_playlist_manage_shows(context.token, playlist_type='RELEASE_MATCH',
                                                                          automatically_apply=automatically_apply,
                                                                          playlist_uuid=playlist_uuid,
                                                                          show_attribute=show_attribute)
    context.resp = res.json()
    return context.resp


def query_auto_playlist_manage_shows(context, playlist_uuid):
    res = Playlist(context.producer_view_url).query_playlist_manage_shows(context.token, playlist_type='RELEASE_MATCH',
                                                                          automatically_apply=True,
                                                                          playlist_uuid=playlist_uuid)
    context.resp = res.json()
    return context.resp


def query_process_queues(context, name, sections=[], status=[]):
    res = Playlist(context.playlist_url).query_process_queues(context.token, name=name, sections=sections,
                                                              status=status)
    context.resp = res.json()
    return context.resp
