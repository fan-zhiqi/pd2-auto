from features.constants import PRODUCER2_URI,PRODUCER2_PORTS
from features.constants import PRODUCER2_CPL_URL

def get_cpl_url(context):
    context.cpl_url = PRODUCER2_URI + PRODUCER2_PORTS['content']
    context.cpl_detail_url = PRODUCER2_URI + PRODUCER2_PORTS['cpl_detail']