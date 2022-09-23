import time
from retrying import retry

import features.steps.api.other as api_others
import logging as log



@retry(wait_fixed=5000, stop_max_attempt_number=10)
def assert_kdm_available_on_unassigned_device_api(
        context, actor, dnqualifier, recipient_name,
        status, total_kdms):
    """ Assert the API endpoint correctly returns unassigned devices with
    correct information relating to the kdm

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param dnqualifier: dnqualifier of kdm
    :type  dnqualifier: str
    :param recipient_name: name of kdm
    :type  recipient_name: str
    :param status: status of kdm - linked to unassigned devices section
    :type  status: str
    :param total_kdms: total value of kdms
    :type  total_kdms: int
    """
    time.sleep(10)
    unassigned_device = api_others.get_unassigned_device_by_name(
        context,
        actor,
        unassigned_device_name=recipient_name
    )

    assert unassigned_device['dnqualifier'] == dnqualifier, \
        f"Expected: {dnqualifier}, but got: {unassigned_device['dnqualifier']}"

    assert unassigned_device['name'] == recipient_name, \
        f"Expected: {recipient_name}, but got: {unassigned_device['name']}"

    assert unassigned_device['status'] == status, \
        f"Expected: {status}, but got: {unassigned_device['status']}"

    assert unassigned_device['KDMCount'] == total_kdms, \
        f"Expected: {total_kdms}, but got: {unassigned_device['KDMCount']}"


@retry(wait_fixed=5000, stop_max_attempt_number=10)
def assert_kdm_available_on_assigned_device_api(
        context, actor, total_kdms, total_devices, alias_name):
    """ Assert the API endpoint correctly returns assigned devices with
    correct information relating to the kdm

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param total_kdms: total number of kdms assigned
    :type  total_kdms: int
    :param total_devices: total number of devices assigned to site alias
    :type  total_devices: int
    :param alias_name: Name of the alias
    :type  alias_name: string
    """
    time.sleep(10)
    assigned_device = api_others.get_assigned_device_by_name(
        context,
        actor,
        assigned_device_name=alias_name
    )

    assert assigned_device['name'] == alias_name, \
        f"Expected: {alias_name}, but got: {assigned_device['name']}"

    assert assigned_device['deviceCount'] == total_devices, \
        f"Expected: {total_devices}, but got: {assigned_device['deviceCount']}"

    assert assigned_device['KDMCount'] == total_kdms, \
        f"Expected: {total_kdms}, but got: {assigned_device['KDMCount']}"


def assert_add_static_playlist(context, code):
    assert str(context.code) == code
    log.info("assert_add_static_playlist context.code:{0}".format(context.code))


