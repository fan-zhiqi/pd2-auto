import sys
import os
import time

from features.clean_up import logout

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


import logging as log
from os import path
from pprint import pformat
#
# import features.clean_up as clean_up
import features.setup as setup
from features.constants import SERVICE_HOSTS, SERVICE_PORTS
from features.tuples import ScenarioData, NetworkData
from features.constants import MYSQL_DB, POSTGRESQL_DB
from behave.fixture import fixture, use_fixture_by_tag
from features.steps.shows.kafka_util.kafka_cleint import Kafka_producer, Kafka_consumer
# import database as db


def get_network_data():
    """ Get a named tuple instance NetworkData containing the network data
    required for running tests in the environment.8

    :return: Network Data
    :rtype: namedtuple
    """
    minio_url = f"{SERVICE_HOSTS['minio']}:{SERVICE_PORTS['minio']}"
    api_url = f"{SERVICE_HOSTS['api']}:{SERVICE_PORTS['api']}"
    rabbit = f"amqp://{SERVICE_HOSTS['rabbit']}:rabbit@rabbit//"
    rabbit_api = f"{SERVICE_HOSTS['rabbit']}:{SERVICE_PORTS['rabbit']}/api/"

    return NetworkData(
        minio=minio_url,
        api=api_url,
        rabbit=rabbit,
        rabbit_api=rabbit_api
    )


def initialize_loggers(output_dir):
    """Initialize file (and console) loggers."""

    logger = log.getLogger()
    logger.setLevel(log.DEBUG)

    # create debug file handler and set level to debug
    handler = log.FileHandler(
        path.join(output_dir, "behave.log"),
        "w",
        encoding="UTF-8"
    )

    handler.setLevel(log.DEBUG)
    formatter = log.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)


def empty_scenario_data():
    """ Get an empty scenario data (usually for a fresh run) """
    return ScenarioData(actors=[], buckets=[], files=[], tokens=[], aliases=[])


def before_all(context):
    """ Run before any scenarios are run """
    # initialize_loggers("./reports")
    context.success = True
    # context.playlist_session = db.set_up(MYSQL_DB, 'playlist')
    # context.producer_view_session = db.set_up(MYSQL_DB, 'producer_view_service')
    # context.cpl_service_session = db.set_up(POSTGRESQL_DB, 'cpl_service')
    # context.pos_service_session = db.get_postgresql_engine('pos_service')
    # context.complex_service_session = db.get_postgresql_engine('complex_service')
    # initialize_loggers("../../../reports")
    # context.scenario_data = empty_scenario_data()
    # context.network = get_network_data()
    # setup.wait_for_service(context.network.api)
    # setup.wait_for_service(
    #     context.network.rabbit_api,
    #     tries=100,
    #     auth=('rabbit', 'rabbit')
    # )
    # setup.wait_for_celery_consumers_in_rabbit(tries=20)
    # setup.create_multiple_env_variable_buckets(context)
    # setup.wait_for_producer_login()


def before_scenario(context, scenario):
    context.token = setup.wait_for_producer_login()


def after_scenario(context, scenario):
    """ Run after each scenario """

    log.debug(
        "Scenario data after scenario and before the clean up:\n%s",
        # pformat(context.scenario_data._asdict())
    )

    # clean_up.delete_uploaded_files(context)
    # clean_up.delete_created_buckets(context)
    # clean_up.logout(context)
    #
    # log.debug(
    #     '\n*\n* End of scenario: %s !!!!\n%s\n\n\n', scenario.name, (80 * '*'))


# def after_step(context, step):
#     time.sleep(2)

#
# @fixture
# def kafkaproducer(context):
#     context.kafka_producer = Kafka_producer()
#
#
#
# @fixture
# def kafkaconsumer(context):
#     context.kafka_consumer = Kafka_consumer()
#
# fixture_registry={
#     "fixture.kafkaproducer": kafkaproducer,
#     "fixture.kafkaconsumer": kafkaconsumer,
# }
#
# def before_tag(context, tag):
#     if tag.startswith("fixture."):
#         return use_fixture_by_tag(tag, context, fixture_registry)
