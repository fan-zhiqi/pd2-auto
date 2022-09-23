import behave.runner

from features.steps.api.api_utils.api_client import ProducerFrontendServiceAPI
from features.steps.context_management import add_to_scenario_data
from features.tuples import Actor
from features.constants import PRODUCER2_URI,PRODUCER2_PORTS


def get_frontend_service_client(
        context: behave.runner.Context, alias: str
) -> None:
    """ Get a frontend service client to interact with the frontend service
    api, add it to the test context as an actor

    :param context: behave Context
    :param alias: Alias to give the actor who represents the client
    """

    url = f'http://{context.network.api}'

    client = ProducerFrontendServiceAPI(base_url=url)

    actor = Actor(
        alias=alias,
        client=client,
        type='api'
    )
    add_to_scenario_data(context, what=actor, where='actors')


def get_playlist_url(context):
    context.playlist_url = PRODUCER2_URI + PRODUCER2_PORTS['playlist']


def get_title_url(context):
    context.title_url = PRODUCER2_URI + PRODUCER2_PORTS['title']

