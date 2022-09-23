from features.constants import PRODUCER2_URI, PRODUCER2_PORTS


def get_site_url(context):
    context.site_url = PRODUCER2_URI + PRODUCER2_PORTS['site']


def get_user_url(context):
    context.user_url = PRODUCER2_URI + PRODUCER2_PORTS['user']