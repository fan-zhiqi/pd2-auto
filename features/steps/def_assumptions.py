#!/usr/bin/python
#-*-coding:utf-8 -*-
from behave import given

import features.steps.api.assumptions as api_assume
import features.steps.celery_steps.assumptions as celery_assume
import features.steps.s3.assumptions as s3_assume
from features.steps.api.assumptions import get_playlist_url
from features.steps.content.assumptions import get_content_url, get_producer_view_url
from features.steps.cpl.assumptions import get_cpl_url
from features.steps.playlist.assumptions import get_pos_sv_url
from features.steps.site.assumptions import get_site_url, get_user_url


@given('an s3 client called "{alias}"')
def add_s3_client(context, alias):
    s3_assume.get_s3_client(context, alias)


@given('a frontend service client called "{alias}"')
def add_frontend_service_client(context, alias):
    api_assume.get_frontend_service_client(context, alias)


@given('a celery instance called "{alias}"')
def add_celery_instance(context, alias):
    celery_assume.create_celery_instance(context, alias)


@given('获取playlist访问地址')
def add_playlist_url(context):
    get_playlist_url(context)


@given('获取pos_sv访问地址')
def add_pos_uuid_url(context):
    get_pos_sv_url(context)

@given('获取playlist_segment访问地址')
def get_fill_cpl_playlist(context):
    get_pos_sv_url(context)

@given('获取cpl访问地址')
def set_cpl_url(context):
    get_cpl_url(context)

@given('获取title访问地址')
def set_title_url(context):
    api_assume.get_title_url(context)


@given('获取content访问地址')
def set_content_url(context):
    get_content_url(context)


@given('获取site访问地址')
def set_site_url(context):
    get_site_url(context)

@given('获取user访问地址')
def set_user_url(context):
    get_user_url(context)

@given('获取producer_view访问地址')
def set_producer_view_url(context):
    get_producer_view_url(context)

