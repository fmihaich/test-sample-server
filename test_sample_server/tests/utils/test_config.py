import pytest

from assertpy import assert_that
from mock import patch, Mock, ANY

from utils.config.config import Config
from utils.config.config_errors import LoadConfigError, ConfigKeyError
from utils.config.config_sections import ConfigSection, ServerKey, DbKey, LogKey


@patch('utils.config.config.ConfigObj')
class TestConfig(object):

    def test_config_creates_a_config_object_using_the_provided_path(self, config_obj_patch):
        config_path = Mock()
        Config(config_path)
        config_obj_patch.assert_called_once_with(config_path, file_error=True)

    @pytest.mark.parametrize("read_config_error", [
        OSError('Test OS error when reading config file'),
        IOError('Test IO error when reading config file')
    ])
    def test_config_raises_load_config_error_when_error_reading_config_file(self, config_obj_patch, read_config_error):
        config_obj_patch.side_effect = read_config_error
        with pytest.raises(LoadConfigError):
            Config(config_path=ANY)

    @pytest.mark.parametrize("read_config_error", [
        OSError('Test OS error when reading config file'),
        IOError('Test IO error when reading config file')
    ])
    def test_config_raises_load_config_error_when_error_reading_config_file(self, config_obj_patch, read_config_error):
        config_obj_patch.side_effect = read_config_error
        with pytest.raises(LoadConfigError):
            Config(config_path=ANY)

    @patch('utils.config.config.os')
    @pytest.mark.parametrize("get_config_value_method,config_section,path_key", [
        (lambda c: c.log_path, ConfigSection.LOGS, LogKey.PATH),
        (lambda c: c.db_path,  ConfigSection.DB, DbKey.PATH)
    ])
    def test_get_config_path_value_returns_abs_config_obj_path_by_getting_path_from_config_section(
            self, os_patch, config_obj_patch, get_config_value_method, config_section, path_key):
        path_value = Mock()
        config_obj_patch.return_value.__getitem__.return_value = {path_key: path_value}

        config = Config(config_path=ANY)

        assert_that(get_config_value_method(config)).is_equal_to(os_patch.path.abspath.return_value)
        os_patch.path.abspath.assert_called_once_with(path_value)
        config_obj_patch.return_value.__getitem__.assert_called_once_with(config_section)

    @pytest.mark.parametrize("get_config_value_method,config_section,section_key", [
        (lambda c: c.log_level, ConfigSection.LOGS, LogKey.LEVEL),
        (lambda c: c.server_host, ConfigSection.SERVER, ServerKey.HOST),
        (lambda c: c.server_port, ConfigSection.SERVER, ServerKey.PORT)
    ])
    def test_get_config_value_returns_config_obj_value_by_getting_key_from_config_section(
            self, config_obj_patch, get_config_value_method, config_section, section_key):
        section_value = Mock()
        config_obj_patch.return_value.__getitem__.return_value = {section_key: section_value}

        config = Config(config_path=ANY)

        assert_that(get_config_value_method(config)).is_equal_to(section_value)
        config_obj_patch.return_value.__getitem__.assert_called_once_with(config_section)

    @pytest.mark.parametrize("get_config_value_method,config_section", [
        (lambda c: c.log_level, ConfigSection.LOGS),
        (lambda c: c.server_host, ConfigSection.SERVER),
        (lambda c: c.db_path,  ConfigSection.DB)
    ])
    def test_config_value_raises_config_key_error_when_getting_config_obj_section_fails(
            self, config_obj_patch, get_config_value_method, config_section):
        config_obj_patch.return_value.__getitem__.side_effect = KeyError('Testing config obj key error')

        config = Config(config_path=ANY)
        with pytest.raises(ConfigKeyError):
            get_config_value_method(config)

        config_obj_patch.return_value.__getitem__.assert_called_once_with(config_section)

    @pytest.mark.parametrize("get_config_value_method,config_section", [
        (lambda c: c.log_path, ConfigSection.LOGS),
        (lambda c: c.server_port, ConfigSection.SERVER),
        (lambda c: c.db_path,  ConfigSection.DB)
    ])
    def test_config_value_raises_config_key_error_when_missing_key_in_config_obj_section_fails(
            self, config_obj_patch, get_config_value_method, config_section):
        config_obj_patch.return_value.__getitem__.return_value = {'INVALID_KEY': Mock()}

        config = Config(config_path=ANY)
        with pytest.raises(ConfigKeyError):
            get_config_value_method(config)

        config_obj_patch.return_value.__getitem__.assert_called_once_with(config_section)
