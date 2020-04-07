import json
import logging

from behave import step
from hamcrest import assert_that, is_, has_length

from tests.system.test_sample_server.utils.user_mgmt import get_user_from_context


STATUS_CODE = {
    'HTTP_CREATED': 201,
    'HTTP_OK':  200,
    'HTTP_SERVER_ERROR': 500
}


@step(u'I get "{expected_code}" status code')
def check_response_status_code(context, expected_code):
    assert_that(context.response.status_code, is_(STATUS_CODE[expected_code]))


@step(u'All the recent added users are returned')
def check_all_users_are_returned(context):
    server_users = _get_users_from_server_response(server_response=context.response)
    for user_id in context.users.keys():
        user = get_user_from_context(context, user_id)
        _assert_user_is_in_server(server_users, user)


@step(u'I see only "{user_count:d}" user with "{user_id}" "{user_data}"')
def check_exactly_stored_user_data(context, user_count, user_id, user_data):
    server_users = _get_users_from_server_response(server_response=context.response)
    user = get_user_from_context(context, user_id)
    expected_info = {user_data: user[user_data]}
    _assert_user_is_in_server(server_users, user_info=expected_info, count=user_count)


@step(u'The user is not returned')
def check_user_is_not_returned(context):
    server_users = _get_users_from_server_response(server_response=context.response)
    user = get_user_from_context(context)
    _assert_user_is_in_server(server_users, user, count=0)


def _get_users_from_server_response(server_response):
    assert_that(server_response.status_code, is_(STATUS_CODE['HTTP_OK']))
    server_users = json.loads(server_response.content)
    logging.info('Get users response content: "{0}"'.format(server_users))
    return server_users


def _assert_user_is_in_server(server_users, user_info, count=1):
    server_users_matching_condition = \
        [user for user in server_users if all(user[data] == user_info[data] for data in user_info.keys())]
    logging.info('Server users with expected info: "{0}'.format(server_users_matching_condition))
    assert_that(server_users_matching_condition, has_length(count))
