import json
import random
import string
import logging as log

from features.steps.context_management import get_actor_client, \
    add_to_scenario_data
from features.steps.playlist.playlist_utils.playlist_client import Playlist
from features.tuples import Token
import features.steps.api.other as api_others


def login(context, actor, email_address, password):
    """ User can login to Producer Frontend

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param email_address: Name of the email address/username
    :type  email_address: string
    :param password: Name of the password
    :type  password: string
    """
    login_data = {
        "email": email_address,
        "password": password
    }

    client = get_actor_client(context, actor)
    response = client.v1.login(arguments=login_data)

    auth_token = response.cookies['refresh_token'].replace("'", "")

    token = Token(
        alias=email_address,
        actor=actor,
        email=email_address,
        token=auth_token
    )

    add_to_scenario_data(context, what=token, where='tokens')


def assigning_kdm_to_device(context, actor, recipient_name, alias_name):
    """ Assigning a device for a user

    :param context: behave Context
    :type  context: behave.runner.Context
    :param actor: Name/Alias of the actor
    :type  actor: string
    :param recipient_name: Name of the recipient
    :type  recipient_name: string
    :param alias_name: Name of the alias
    :type  alias_name: string
    :return: Site Alias created response
    """

    unassigned_device_id = api_others.get_unassigned_device_by_name(
        context,
        actor,
        unassigned_device_name=recipient_name
    )['id']

    assign_data = {
        "siteName": alias_name,
        "deviceID": int(unassigned_device_id),
        "screenName": alias_name
    }
    client = get_actor_client(context, actor)

    client.v1.create_site_alias_and_assign_device(
        arguments=assign_data
    )



def get_static_playlist(context,automatically_apply,title):
    titles=title+''.join(random.sample(string.ascii_letters + string.digits, 8))
    data={
         "automatically_apply": automatically_apply,
         "title": titles
     }
    playlist_client=Playlist(context.playlist_url)
    res=playlist_client.create_static_playlist(context.token, data)
    response=json.loads(res.text)
    context.code=response['code']
    log.info("get_static_playlist response status_code :{0},response:{0},context.code:{0}"
             .format(res,response,context.code))
