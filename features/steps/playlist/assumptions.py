from features.constants import PRODUCER2_URI,PRODUCER2_PORTS
def get_pos_sv_url(context):
    context.pos_sv_url = PRODUCER2_URI + PRODUCER2_PORTS['pos-sv']
    context.playlist_url = PRODUCER2_URI + PRODUCER2_PORTS['playlist']
    context.match_playlist_url = PRODUCER2_URI + PRODUCER2_PORTS['matchPlaylist']
    # context.posuuid_url = 'http://k8s-test-1.aamcn.com.cn:' + PRODUCER2_PORTS['showList']
    # context.playlist_url = 'http://k8s-test-1.aamcn.com.cn:' + PRODUCER2_PORTS['playlist']
    # context.match_playlist_url = 'http://k8s-test-1.aamcn.com.cn:' + PRODUCER2_PORTS['matchPlaylist']
