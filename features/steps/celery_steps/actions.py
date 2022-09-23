from features.steps.context_management import get_from_scenario_data

TS_MESSAGING_EXCHANGE = 'ts.messaging'

def handle_asset_task(context, actor, user_name, kdm_name):
    """ Create and send the kdm task 'handle_asset_data'

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param user_name: Name/Alias of the user
    :type  user_name: string
    :param kdm_name: Name of the compressed kdm file
    :type  kdm_name: str
    """
    kdm_data = {
        's3_location': f'jester-assets/{kdm_name}',
        'type': 'kdm',
        'id': 1,
        'users': [user_name]
    }
    send_ingest_handle_asset_task(context, actor, kdm_data)


def send_ingest_handle_asset_task(context, actor, kdm_data):
    """ Send an ingest kdm task to the kdm service using celery

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param kdm_data: kdm info for getting kdm from s3 folder and sending
    :type  kdm_data: dict
    """
    celery = get_from_scenario_data(context, where='actors', name=actor).client

    celery.send_task(
        'handle_asset_data',
        args=({'data': kdm_data},),
        exchange=TS_MESSAGING_EXCHANGE,
        routing_key='asset.data'
    )
