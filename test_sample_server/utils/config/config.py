import os

from configobj import ConfigObj

from utils.config.config_errors import LoadConfigError, ConfigKeyError
from utils.config.config_sections import ConfigSection, ServerKey, DbKey, LogKey


class Config(object):
    def __init__(self, config_path):
        try:
            self._conf = ConfigObj(config_path, file_error=True)
        except (OSError, IOError) as e:
            raise LoadConfigError(str(e))

    @property
    def log_path(self):
        return os.path.abspath(self._get_config_key(ConfigSection.LOGS, LogKey.PATH))

    @property
    def log_level(self):
        return self._get_config_key(ConfigSection.LOGS, LogKey.LEVEL)

    @property
    def db_path(self):
        return os.path.abspath(self._get_config_key(ConfigSection.DB, DbKey.PATH))

    @property
    def server_host(self):
        return self._get_config_key(ConfigSection.SERVER, ServerKey.HOST)

    @property
    def server_port(self):
        return self._get_config_key(ConfigSection.SERVER, ServerKey.PORT)

    def _get_config_key(self, section, key):
        try:
            return self._conf[section][key]
        except KeyError as e:
            raise ConfigKeyError('[{0}][{1}] key not defined in server config:\n{0}'.format(section, key, str(e)))
