import json
import logging
import requests

from behave import step
from random import randint

from tests.system.test_sample_server.utils.user_mgmt import DEFAULT_USER_ID, get_user_from_context


SERVER_ADD_USER_URL = '{server_url}/user/add'
SERVER_GET_USERS_URL = '{server_url}/users'


@step(u'I add "{user_id}" user')
def add_user(context, user_id=DEFAULT_USER_ID):
    user = get_user_from_context(context, user_id)
    logging.info('Adding user which id is: "{0}"'.format(user_id))
    context.response = _perform_add_user_request(server_url=context.server_url, user_data=json.dumps(user))


@step(u'I successfully add "{user_count:d}" users')
def add_users(context, user_count):
    user_id_prefix = 'user_{0}'.format(randint(0, 1000000))
    for i in range(1, user_count+1):
        user_id = user_id_prefix + '_{0}'.format(i)
        context.execute_steps(u'''
            Given I add "{0}" user
            Then I get "HTTP_CREATED" status code'''.format(user_id))


@step(u'I try to add other user which "{user_data}" is the same than "{base_user_id}" username')
def add_user_again_with_specific_data(context, user_data, base_user_id):
    new_user_id = 'new_user_{0}'.format(randint(0, 1000000))
    new_user = get_user_from_context(context, user_id=new_user_id)
    base_user = get_user_from_context(context, user_id=base_user_id)
    new_user[user_data] = base_user[user_data]

    logging.info('Adding user which id is: "{0}"'.format(new_user_id))
    context.response = _perform_add_user_request(server_url=context.server_url, user_data=json.dumps(new_user))


@step(u'I try to add a user without specifying the "{missing_data}"')
def add_user_with_missing_data(context, missing_data):
    user = get_user_from_context(context)
    del user[missing_data]
    logging.info('Trying to add a user without "{0}"'.format(missing_data))
    context.response = _perform_add_user_request(server_url=context.server_url, user_data=json.dumps(user))


@step(u'I try to add a user with incomplete data')
def add_user_with_incomplete_data(context):
    user = get_user_from_context(context)
    incomplete_user_data = json.dumps(user)[:-3]
    logging.info('Trying to add a user with incomplete data')
    context.response = _perform_add_user_request(server_url=context.server_url, user_data=incomplete_user_data)


@step(u'I get all users')
def get_users(context):
    request_url = SERVER_GET_USERS_URL.format(server_url=context.server_url)
    logging.info('Get users url: "{0}"'.format(request_url))
    try:
        context.response = requests.get(request_url)
    except Exception as e:
        error_msg = 'Error getting users\n{0}'.format(str(e))
        logging.exception(error_msg)
        assert False, error_msg


def _perform_add_user_request(server_url, user_data):
    request_url = SERVER_ADD_USER_URL.format(server_url=server_url)
    logging.info('Add user url: "{0}"'.format(request_url))
    logging.info('Add user body: "{0}"'.format(user_data))

    try:
        response = requests.post(request_url, data=user_data, headers={"Content-Type" : "application/json"})
    except Exception as e:
        logging.exception('Add user request error:\n{0}'.format(str(e)))
        return False

    logging.info('Add user response: "{0}"'.format(response))
    return response
