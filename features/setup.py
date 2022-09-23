
from tools.logger import GetLogger
log=GetLogger().get_logger()

import time
from os import getenv
from time import sleep

import requests

import features.constants as constants
from features.steps.s3.s3_utils.s3_client import S3Client
from features.steps.api.api_utils.v1 import V1
from features.constants import PRODUCER2_URI, PRODUCER2_PORTS, PRODUCER2


def create_multiple_env_variable_buckets(context):
    """ Create multiple s3 buckets for testing

    :param context: behave Context
    :type  context: behave.runner.Context
    """
    url = f'http://{context.network.minio}'
    bucket_names = getenv('MINIO_S3_OUTPUT_BUCKET').split(',')

    client = S3Client(
        # url=url,
        access_key=getenv('MINIO_ACCESS_KEY', 'minio'),
        secret_key=getenv('MINIO_SECRET_KEY', 'minio123'),
        **constants.S3_CONFIG
    )

    for bucket_name in bucket_names:
        client.create_bucket(bucket_name=bucket_name)
        client.wait_for_bucket_exists(bucket=bucket_name)


def wait_for_service(url, tries=10, auth=None):
    for i in range(tries):
        try:
            log.info(f'Waiting for {url} ({i})')
            res = requests.get(f'http://{url}', auth=auth)
            code = res.status_code
            success = code == 200
            if success:
                break
        except Exception as e:
            if i == tries - 1:
                raise e
        sleep(1)


def _rabbit_queues_with_consumers(user, password, host, port, vhost=''):
    url = f'http://{host}:{port}/api/consumers/{vhost}'

    log.info(f'Getting rabbit queues with consumers ready for {url}')

    response = requests.get(
        url,
        auth=(user, password)
    )
    queues = {q['queue']['name'] for q in response.json()}
    return queues


def wait_for_celery_consumers_in_rabbit(tries: int=20) -> None:
    """ Wait until rabbit has consumers for the queues used by the cpl
    service. Sending a cpl to rabbit before the celery is ready will
    cause all sorts of mayhem.

    :raises RuntimeError: If celery is not ready to consume from rabbit
    """
    expected_consumer_queues = {
        'kdm_service.default',
        'kdm_service.events',
        'producer_service.default',
        'producer_service.events'
    }

    for i in range(tries):

        success = expected_consumer_queues <= _rabbit_queues_with_consumers(
            user=getenv('RABBITMQ_DEFAULT_USER', 'rabbit'),
            password=getenv('RABBITMQ_DEFAULT_PASS', 'rabbit'),
            host=constants.SERVICE_HOSTS['rabbit'],
            port=constants.SERVICE_PORTS['rabbit']
        )

        if success:
            log.info('Celery ready to consume from rabbit')
            return

        log.info('Celery not ready to consume from cpl service rabbit queues')
        sleep(2)

    raise RuntimeError('Rabbit queue consumers not ready within timeout')



def producer_login():
    data = {
        "username": PRODUCER2["username"],
        "password": PRODUCER2["password"],
        "organization_uuid": constants.organization_uuid
    }
    login_url = PRODUCER2_URI + PRODUCER2_PORTS['user']
    p = V1(login_url)
    s=p.login(data)
    time.sleep(2)

    return s['X-Thunderstorm-Key']

def wait_for_producer_login() -> object:
    success= producer_login()
    if success:
        log.info('producer2 login success')
        return success

    log.info('producer2 login fail')
    sleep(2)

    raise RuntimeError('producer2 login timeout')


if __name__ == '__main__':
    print(producer_login())