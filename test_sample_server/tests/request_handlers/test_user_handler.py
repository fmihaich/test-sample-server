import pytest

from assertpy import assert_that
from mock import patch, Mock

from models.user.user import User
from models.user.user_mgmt_errors import UserInsufficientData, UserInvalidDataType
from request_handlers.user_handler import add_user, get_all_users
from utils.http.http_status import HttpStatus
from utils.db.db import DataBase
from utils.db.db_errors import DataBaseInstanceError, DuplicateUserError, DataBaseInsertionError, DataBaseReadError


@patch('request_handlers.user_handler.json')
@patch('request_handlers.user_handler.logging')
class TestAddUser(object):
    def test_add_user_responses_bad_request_when_malformed_request_body(self, json_mock, logging_mock):
        request = Mock()
        request.body.read.side_effect = Exception('Test - request body read exception')

        response = add_user(request)

        request.body.read.assert_called_once_with()
        assert_that(response.status_code).is_equal_to(HttpStatus.BAD_REQUEST)

    @pytest.mark.parametrize("user_data_error", [
        UserInsufficientData('Test user insufficient data error'),
        UserInvalidDataType('Test user invalid data error')
    ])
    def test_add_user_responses_bad_request_when_error_in_json_data(self, logging_mock, json_mock, user_data_error):
        request = Mock()
        request_user_data = Mock()
        json_mock.loads.return_value = request_user_data

        with patch.object(User, '__init__', side_effect=user_data_error) as user_mock:
            response = add_user(request)
            user_mock.assert_called_once_with(request_user_data)

        assert_that(response.status_code).is_equal_to(HttpStatus.BAD_REQUEST)

    def test_add_user_responses_internal_error_when_getting_db_instance_fails(self, logging_mock, json_mock):
        request = Mock()
        request_user_data = Mock()
        json_mock.loads.return_value = request_user_data

        with patch.object(User, '_get_missing_mandatory_attr', return_value=[]):
            with patch.object(User, '_check_valid_date', return_value=True):
                with patch.object(DataBase, 'get_instance') as db_get_instance_mock:
                    db_get_instance_mock.side_effect = DataBaseInstanceError('Test DB get instance error')
                    response = add_user(request)
                    db_get_instance_mock.assert_called_once_with()

        assert_that(response.status_code).is_equal_to(HttpStatus.INTERNAL_ERROR)

    @pytest.mark.parametrize("db_error", [
        DuplicateUserError('Test DB duplicate user error'),
        DataBaseInsertionError('Test DB insertion error')
    ])
    def test_add_user_responses_internal_error_when_insert_a_user_in_db_fails(self, logging_mock, json_mock, db_error):
        request = Mock()
        request_user_data = Mock()
        json_mock.loads.return_value = request_user_data

        with patch.object(User, '_get_missing_mandatory_attr', return_value=[]):
            with patch.object(User, '_check_valid_date', return_value=True):
                with patch.object(DataBase, 'get_instance') as db_get_instance_mock:
                    db_instance_mock = Mock()
                    db_instance_mock.insert_user.side_effect = db_error
                    db_get_instance_mock.return_value = db_instance_mock

                    response = add_user(request)
                    db_instance_mock.insert_user.assert_called_once()

        assert_that(response.status_code).is_equal_to(HttpStatus.INTERNAL_ERROR)

    def test_add_user_responses_ok_status_code_when_user_is_correctly_stored_in_db(self, logging_mock, json_mock):
        request = Mock()
        request_user_data = Mock()
        json_mock.loads.return_value = request_user_data

        with patch.object(User, '_get_missing_mandatory_attr', return_value=[]):
            with patch.object(User, '_check_valid_date', return_value=True):
                with patch.object(DataBase, 'get_instance') as db_get_instance_mock:
                    db_instance_mock = Mock()
                    db_instance_mock.side_effect = None
                    db_get_instance_mock.return_value = db_instance_mock

                    response = add_user(request)
                    db_instance_mock.insert_user.assert_called_once()

        assert_that(response.status_code).is_equal_to(HttpStatus.CREATED)


@patch('request_handlers.user_handler.logging')
class TestGetAllUsers(object):

    def test_get_all_users_responses_internal_error_when_getting_db_instance_fails(self, logging_mock):
        with patch.object(DataBase, 'get_instance') as db_get_instance_mock:
            db_get_instance_mock.side_effect = DataBaseInstanceError('Test DB get instance error')
            response = get_all_users()
            db_get_instance_mock.assert_called_once_with()

        assert_that(response.status_code).is_equal_to(HttpStatus.INTERNAL_ERROR)

    def test_get_all_users_responses_internal_error_when_read_users_from_db_fails(self, logging_mock):
        with patch.object(DataBase, 'get_instance') as db_get_instance_mock:
            db_instance_mock = Mock()
            db_instance_mock.get_all_users.side_effect = DataBaseReadError('Test DB read error')
            db_get_instance_mock.return_value = db_instance_mock

            response = get_all_users()
            db_instance_mock.get_all_users.assert_called_once_with()

        assert_that(response.status_code).is_equal_to(HttpStatus.INTERNAL_ERROR)

    @patch('request_handlers.user_handler.json')
    def test_get_all_users_responses_ok_status_code_when_there_is_no_error_getting_them(self, json_mock, logging_mock):
        with patch.object(DataBase, 'get_instance') as db_get_instance_mock:
            all_stored_users = [Mock(), Mock(), Mock()]
            db_instance_mock = Mock()
            db_instance_mock.get_all_users.return_value = all_stored_users
            db_get_instance_mock.return_value = db_instance_mock

            response = get_all_users()
            db_instance_mock.get_all_users.assert_called_once_with()

        json_mock.dumps.assert_called_once()
        assert_that(response.status_code).is_equal_to(HttpStatus.OK)
