import pytest

from mock import patch, Mock, ANY

from server import server_main, add_new_user, get_users

@patch('server.os')
@patch('server.ArgumentParser')
@patch('server.Config')
@patch('server.logging')
@patch('server.DataBase')
@patch('server.run')
class TestServerMain(object):
    def test_server_main_initializes_config_with_args_parser_config_arg(
            self, bottle_run_patch, db_patch, logging_patch, config_patch, arg_parser_patch, os_patch):
        server_main()
        arg_parser_patch.return_value.parse_args.assert_called_once()
        config_patch.assert_called_once_with(arg_parser_patch.return_value.parse_args.return_value.config)

    def test_server_main_initializes_logging_with_config_logs_arguments(
            self, bottle_run_patch, db_patch, logging_patch, config_patch, arg_parser_patch, os_patch):
        configured_log_path = Mock()
        configured_log_level = Mock()

        config_patch.return_value.log_path = configured_log_path
        config_patch.return_value.log_level = configured_log_level

        server_main()

        logging_patch.basicConfig.assert_called_once_with(filename=configured_log_path, format=ANY)
        logging_patch.getLogger.return_value.setLevel.assert_called_once_with(configured_log_level)

    def test_server_main_loads_db_with_config_db_argument(
            self, bottle_run_patch, db_patch, logging_patch, config_patch, arg_parser_patch, os_patch):
        configured_db_path = Mock()
        config_patch.return_value.db_path = configured_db_path

        server_main()

        db_patch.get_instance.assert_called_once_with(configured_db_path)

    def test_server_main_runs_server_with_config_server_arguments_when_no_initialization_errors(
            self, bottle_run_patch, db_patch, logging_patch, config_patch, arg_parser_patch, os_patch):
        configured_server_host = Mock()
        configured_server_port = Mock()

        config_patch.return_value.server_host = configured_server_host
        config_patch.return_value.server_port = configured_server_port

        server_main()
        bottle_run_patch.assert_called_once_with(host=configured_server_host, port=configured_server_port, debug=ANY)

    @patch('server.user_handler.add_user')
    @patch('server.request')
    def test_add_new_user_returns_user_handler_add_user_result(
            self, request_patch, add_user_handler_path,
            bottle_run_patch, db_patch, logging_patch, config_patch, arg_parser_patch, os_patch):
        add_new_user()
        add_user_handler_path.assert_called_once_with(request_patch)

    @patch('server.user_handler.get_all_users')
    @patch('server.request')
    def test_get_users_returns_user_handler_get_all_users_result(
            self, request_patch, get_all_users_patch,
            bottle_run_patch, db_patch, logging_patch, config_patch, arg_parser_patch, os_patch):
        get_users()
        get_all_users_patch.assert_called_once_with()
