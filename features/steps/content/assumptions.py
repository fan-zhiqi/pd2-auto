from features.constants import PRODUCER2_URI, PRODUCER2_PORTS


def get_content_url(context):
    context.content_url = PRODUCER2_URI + PRODUCER2_PORTS['content']


def get_producer_view_url(context):
    context.producer_view_url = PRODUCER2_URI + PRODUCER2_PORTS['pv-sv']
