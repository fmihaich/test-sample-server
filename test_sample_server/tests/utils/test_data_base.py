import pytest

from assertpy import assert_that
from mock import patch, Mock, ANY

from utils.db.db import DataBase
from utils.db.db_errors import DataBaseInstanceError, DataBaseInsertionError, DuplicateUserError, DataBaseReadError


@patch('utils.db.db.TinyDB')
class TestDataBase(object):

    def test_db_instantiation_raises_db_instance_error_when_db_load_fails(self, tiny_db_mock):
        tiny_db_mock.side_effect = Exception('Tiny DB test Exception')
        with pytest.raises(DataBaseInstanceError):
            DataBase.get_instance(ANY)

    def test_db_instance_loads_a_db_from_provided_path(self, tiny_db_mock):
        db_path = '/test/path/some_db.json'
        DataBase.get_instance(db_path)
        tiny_db_mock.assert_called_once_with(db_path)

    def test_db_instantiation_twice_raises_an_instance_error(self, tiny_db_mock):
        DataBase.get_instance()
        with pytest.raises(DataBaseInstanceError):
            DataBase(db_path=ANY)

    def test_db_insert_user_stores_a_user_when_its_username_does_not_exist(self, tiny_db_mock):
        db = DataBase.get_instance(ANY)
        db._db = Mock()
        db._db.search.return_value = []

        user = Mock()

        db.insert_user(user)
        db._db.search.assert_called_once()
        db._db.insert.assert_called_once_with(user.data)

    def test_db_insert_user_does_not_store_a_user_when_its_username_does_exist(self, tiny_db_mock):
        db = DataBase.get_instance(ANY)
        db._db = Mock()

        user = Mock()
        db._db.search.return_value = [user.data]

        with pytest.raises(DuplicateUserError):
            db.insert_user(user)

        db._db.search.assert_called_once()
        db._db.insert.assert_not_called()

    def test_db_insert_user_does_not_store_a_user_when_the_insertion_fails(self, tiny_db_mock):
        db = DataBase.get_instance(ANY)
        db._db = Mock()
        db._db.search.return_value = []
        db._db.insert.side_effect = Exception('Test DB insertion exception')

        user = Mock()

        with pytest.raises(DataBaseInsertionError):
            db.insert_user(user)

        db._db.search.assert_called_once()
        db._db.insert.assert_called_once_with(user.data)

    @pytest.mark.parametrize("stored_users", [[], [Mock(), Mock()]])
    def test_db_get_all_users_returns_stored_users_when_get_all_users_works_ok(self, tiny_db_mock, stored_users):
        db = DataBase.get_instance(ANY)
        db._db = Mock()
        db._db.all.return_value = stored_users

        current_stored_users = db.get_all_users()

        db._db.all.assert_called_once_with()
        assert_that(current_stored_users).is_length(len(stored_users))
        for stored_user in stored_users:
            assert_that(current_stored_users).contains(stored_user)

    def test_db_get_all_users_raises_db_read_error_when_read_all_users_fails(self, tiny_db_mock):
        db = DataBase.get_instance(ANY)
        db._db = Mock()
        db._db.all.side_effect = Exception('Test DB get all exception')

        with pytest.raises(DataBaseReadError):
            db.get_all_users()
        db._db.all.assert_called_once_with()
