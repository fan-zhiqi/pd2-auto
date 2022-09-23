import logging as log
import json
from features.steps.cpl.cpl_utils.segment_cpl import SegmentCpl


def check_cpl_update_segment_success(context, cpl_uuid: str):
    detail = SegmentCpl(context.cpl_detail_url)
    res = detail.get_cpl_detail(cpl_uuid.strip(), context.token)
    respose = json.loads(res.content)
    cpl_u_data = json.loads(context.cpl_u_data)
    if cpl_u_data['cpl_uuids'][0] == respose['data']['uuid']:
        if len(cpl_u_data['ratings']) <= 0:
            if cpl_u_data['producer_credit_offset'] == respose['data']['producer_credit_offset']:
                log.info("检查cpl修改成功{0}".format(cpl_uuid))
        else:
            if cpl_u_data['ratings'][0]['rating_value'] == respose['data']['rating'][0]['rating'] and cpl_u_data['ratings'][0]['territory'] == respose['data']['rating'][0]['territory']:
                log.info("检查cpl修改成功{0}".format(cpl_uuid))
    else:
        log.info("检查cpl修改失败")



def assert_edit_cpl_intermission_value_result(context, intermission_value):
    assert str(context.intermission) == intermission_value
    log.info(f'修改cpl intermission value, result intermission_value:{intermission_value}')



