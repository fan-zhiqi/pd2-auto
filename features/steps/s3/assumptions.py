from os import getenv

from features.constants import S3_CONFIG
from features.steps.context_management import add_to_scenario_data
from features.steps.s3.s3_utils.s3_client import S3Client
from features.tuples import Actor


def get_s3_client(
        context,
        alias,
        access_key=getenv('MINIO_ACCESS_KEY', 'minio'),
        secret_key=getenv('MINIO_SECRET_KEY', 'minio123'),
        config=S3_CONFIG
):
    """ Get an s3 client to interact with the S3 instance using AWS boto3,
    add it to the test context as an actor

    :param context: behave Context
    :type  context: behave.runner.Context
    :param alias: Alias to give the actor
    :type  alias: string
    :param access_key: access key for s3 instance
    :type  access_key: str
    :param secret_key: secret key for s3
    :type  secret_key: str
    :param config: config parameters for s3 client
    :type  config: dict
    """

    url = 'http://' + context.network.minio

    client = S3Client(
        url=url,
        access_key=access_key,
        secret_key=secret_key,
        **config
    )

    actor = Actor(
        alias=alias,
        client=client,
        type='minio'
    )

    add_to_scenario_data(context, what=actor, where='actors')
