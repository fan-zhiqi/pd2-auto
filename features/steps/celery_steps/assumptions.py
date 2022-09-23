from celery import Celery

from features.steps.context_management import add_to_scenario_data
from features.tuples import Actor


def create_celery_instance(context, actor):
    """ Get an instance of celery to use as an actor. This can be used to
    send tasks to rabbit.

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias to give the actor
    :type  actor: string
    """
    app = Celery(broker=context.network.rabbit)
    celery_actor = Actor(actor, app, 'celery')
    add_to_scenario_data(context, what=celery_actor, where='actors')
