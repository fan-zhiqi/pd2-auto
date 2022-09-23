from features.steps.context_management import get_actor_client


def get_unassigned_devices(context, actor):
    """ Get a list of Unassigned Devices from graphGL, which connects to
    kdm-service and producer-service

    param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Alias to give the actor
    :type  actor: string
    :return: list of Unassigned Devices
    :rtype: list
    """
    client = get_actor_client(context, actor)

    unassigned_devices = client.graphQL.get_unassigned_devices()

    return unassigned_devices['data']['unassignedDevices']


def get_assigned_devices(context, actor):
    """ Get a list of Assigned Devices from graphGL, which connects to
    kdm-service and producer-service

    param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Alias to give the actor
    :type  actor: string
    :return: list of Assigned Devices
    :rtype: list
    """
    client = get_actor_client(context, actor)

    assigned_devices = client.graphQL.get_assigned_devices()

    return assigned_devices['data']['sites']


def get_site_aliases(context, actor):
    """ Get a list of Site Aliases from graphGL, which connects to
    kdm-service and producer-service

    param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Alias to give the actor
    :type  actor: string
    :return: list of Site Aliases
    :rtype: list
    """
    client = get_actor_client(context, actor)

    site_aliases = client.graphQL.get_site_aliases()

    return site_aliases['data']['sites']


def get_unassigned_device_by_name(context, actor, unassigned_device_name):
    """ Get unassigned device's information from the end point of the api

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Alias to give the actor
    :type  actor: string
    :param unassigned_device_name: name of unassigned device to return
    :type  unassigned_device_name: str
    :return: unassigned device
    :rtype:  dict
    """
    unassigned_devices = get_unassigned_devices(context, actor)

    return next(
        device for device in unassigned_devices
        if device['name'] == unassigned_device_name
    )


def get_assigned_device_by_name(context, actor, assigned_device_name):
    """ Get assigned device's information from the end point of the api

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Alias to give the actor
    :type  actor: string
    :param assigned_device_name: name of assigned device to return
    :type  assigned_device_name: str
    :return: assigned device
    :rtype:  dict
    """
    assigned_devices = get_assigned_devices(context, actor)

    return next(
        device for device in assigned_devices
        if device['name'] == assigned_device_name
    )


def get_site_aliases_by_name(context, actor, site_alias_name):
    """ Get site alias's information from the end point of the api

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Alias to give the actor
    :type  actor: string
    :param site_alias_name: name of site alias to return
    :type  site_alias_name: str
    :return: site alias
    :rtype:  dict
    """
    site_aliases = get_site_aliases(context, actor)

    return next(
        device for device in site_aliases
        if device['name'] == site_alias_name
    )
