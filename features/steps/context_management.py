#!/usr/bin/python
#-*-coding:utf-8 -*-
from features.steps.utils import is_namedtuple_instance


def add_to_scenario_data(context, what, where):
    """Add given item to specified scenario data bucket.

    :param context: behave Context
    :type  context: behave.runner.Context
    :param what:    name of the item to add
    :type  what:    object
    :param where:   name of the scenario data bucket
    :type  where:   str
    """
    getattr(context.scenario_data, where).append(what)


def get_from_scenario_data(context, where, name):
    """Return data stored in one of the `context.scenario_data` buckets.

    Please refer to `features.tuples.ScenarioData` for the list of all them.

    :param context: behave Context
    :type  context: behave.runner.Context
    :param where: name of the bucket where you want to search
    :type  where: str
    :param name:  name or the alias of the sought item
    :type  name: str
    :return: scenario data for selected item
    :rtype:  namedtuple
    """
    data = getattr(context.scenario_data, where)

    for item in data:

        if isinstance(item, dict):
            if item['alias'] == name:
                return item

        elif is_namedtuple_instance(item):
            if item.alias == name:
                return item

    raise ValueError(
        'Could not find {0} in {1}: {2}'.format(name, where, data))


def delete_from_scenario_data(context, what, where):
    """Delete given item from specified scenario data bucket.

    :param context: behave Context
    :type  context: behave.runner.Context
    :param what:    item to delete from selected scenario data bucket
    :type  what:    dict
    :param where:   name of the scenario data bucket
    :type  where:   str
    """
    getattr(context.scenario_data, where).remove(what)


def get_actor_client(context, actor):
    """Get the client for specified actor.

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type actor: string
    :return: client
    :rtype: client
    """
    actor = get_from_scenario_data(context, where='actors', name=actor)
    return actor.client
