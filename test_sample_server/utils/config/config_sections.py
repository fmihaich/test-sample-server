class ConfigSection(object):
    SERVER = 'server'
    DB = 'db'
    LOGS = 'logs'


class ServerKey(object):
    HOST = 'host'
    PORT = 'port'


class DbKey(object):
    PATH = 'path'


class LogKey(object):
    PATH = 'path'
    LEVEL = 'log_level'
