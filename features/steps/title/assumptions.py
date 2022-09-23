#!/usr/bin/python
#-*-coding:utf-8 -*-
from features.constants import PRODUCER2_URI, PRODUCER2_PORTS


def get_title_url(context):
    context.title_url = PRODUCER2_URI + PRODUCER2_PORTS['title']