import json

from tools.logger import GetLogger
log=GetLogger().get_logger()

from features.steps.cpl.cpl_utils.segment_cpl import SegmentCpl
from features.steps.cpl.cpl_utils.cpl_db_model import CPLLocation
from features.steps.cpl.cpl_utils.cpl_db_connection_util import CPLDBConnection
from sqlalchemy import and_



def update_cpl_segment(context, cpl_update_json, success,token):
    data = json.loads(json.dumps(cpl_update_json))
    log.info('cpl_update_json:{0}'.format(cpl_update_json))
    log.info('cpl_update_json:{0}'.format(type(data)))
    cpl = SegmentCpl(context.cpl_url)
    context.cpl_u_data = cpl_update_json
    res = cpl.update_cpl_segment(json.loads(cpl_update_json), token)
    log.info("res:{0}".format(res))
    log.info("response:{0}".format(res.text))
    log.info("response:{0}".format(type(json.loads(res.text))))

    if success == json.loads(res.text)['code']:
        context.success = True
        log.info(f'修改cpl status_code:{res["code"]}, response:{res}, context_success:{context.success}')


def update_intermission(context, intermission_value):
    data = {
        "cpl_uuids": [
            context.cpl_uuid
        ],
        "intermission": intermission_value
    }
    cpl = SegmentCpl(context.cpl_url)
    res = cpl.update_cpl_segment(data, context.token)
    response = json.loads(res.text)
    if 'message' in response and 'code' in response:
        context.code = response['code']
    log.info(f'修改cpl的intermission value, status_code:{context.code}, response:{response} ')


def get_cpl_detail(context):
    detail = SegmentCpl(context.cpl_detail_url)
    res = detail.get_cpl_detail(context.cpl_uuid, context.token)
    response = json.loads(res.text)
    if 'data' in response and len(response['data']) > 0:
        context.intermission = response['data']['producer_intermission']
    log.info(f'获取到修改后的cpl intermission value, status_code:{context.code}, response:{response} ')


def get_unuse_cpl_uuid(context):
    cpl_client = SegmentCpl(context.cpl_detail_url)
    res = cpl_client.get_cpl_list(context.token)
    response = json.loads(res.text)

    if 'data' not in response or response['code'] != 200 or len(response['data']) < 1:
        log.error(f"delete unUse cpl error ，response={response}")
        raise RuntimeError(f"delete unUse cpl error ，response={response}")

    context.cpl_uuid = response['data'][0]['uuid']


def get_has_device_unuse_cpl_uuid(context):
    cpl_client = SegmentCpl(context.cpl_detail_url)
    res = cpl_client.get_cpl_list(context.token)
    response = json.loads(res.text)

    # if 'data' not in response or response['code'] != 200 or len(response['data']) < 1:
    #     log.error(f"delete unUse cpl error ，response={response}")
    #     raise RuntimeError(f"delete unUse cpl error ，response={response}")
    #
    # context.cpl_uuid = response['data'][0]['uuid']
    data = response['data']
    for item in data:
        response = cpl_client.get_complex_device_uuid(context.token, item['uuid'])
        res = json.loads(response.text)['data']
        if len(res) > 0:
            context.cpl_uuid = item['uuid']
            return
    log.error(f"找不到含有设备的cpl, response={response}")
    raise RuntimeError(f"找不到含有设备的cpl, response={response}")

def get_complex_device_uuid(context):
    cpl_client = SegmentCpl(context.cpl_detail_url)
    res = cpl_client.get_complex_device_uuid(context.token, context.cpl_uuid)
    response = json.loads(res.text)

    if 'data' not in response or response['code'] != 200 or len(response['data']) == 0:
        log.error(f"delete cpl error ,get complex_uuid and device_uuid error  response={response}")
        raise RuntimeError(f"delete cpl error ,get complex_uuid and device_uuid error  response={response}")

    for screen in response['data']:
        if screen['lms'] is not None and 'device_uuid' in screen['lms']:
            context.device_uuid = screen['lms']['device_uuid']
            context.complex_uuid = screen['complex_uuid']
            return

    log.error(f"delete cpl error ，because this cpl lms is all null ，response_data={response['data']}")
    raise RuntimeError(f"delete cpl error ，because this cpl lms is all null ，response_data={response['data']}")


def delete_cpl(context):
    cpl_client = SegmentCpl(context.cpl_url)
    res = cpl_client.delete_cpl(context.complex_uuid, context.cpl_uuid, context.device_uuid, context.token)
    response = json.loads(res.text)

    if 'code' not in response or 'message' not in response or response['code'] != 200 or response['message'] != 'success':
        log.error(f"delete cpl error ,response={response}")
        raise RuntimeError(f"delete cpl error ,response={response}")


def print_db_cpl_service_data(context):
    db = context.cpl_service_session
    result_proxy = db.execute("select error from cpl_location_delete_status where complex_uuid = '" + context.complex_uuid + "' and device_uuid = '" + context.device_uuid + "' and (cpl_uuids::jsonb->>0 = '" + context.cpl_uuid + "')")
    result_list = result_proxy.fetchone()
    if result_list is None:
        log.error(f"delete cpl error , db no exist remove record  cpl_uuid={context.cpl_uuid}  device_uuid={context.device_uuid}  complex_uuid={context.complex_uuid}")
        raise RuntimeError(f"delete cpl error , db no exist remove record  cpl_uuid={context.cpl_uuid}  device_uuid={context.device_uuid}  complex_uuid={context.complex_uuid}")
    else:
        log.info(f"delete cpl db message -------->  error:{result_list[0]}")



