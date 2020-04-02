import logging
import os
from argparse import ArgumentParser

from bottle import get, request, run, post

from request_handlers import user_handler
from utils.config.config import Config
from utils.config.config_errors import LoadConfigError, ConfigKeyError
from utils.db.db import DataBase
from utils.db.db_errors import DataBaseInstanceError


@post('/user/add')
def add_new_user():
    logging.info("\n\n---------------- Add user request ---------------- \n")
    logging.info("URL: {0} \n".format(request.url))
    return user_handler.add_user(request)


@get('/users')
def get_users():
    logging.info("\n\n---------------- All users request ---------------- \n")
    logging.info("URL: {0} \n".format(request.url))
    return user_handler.get_all_users()


def server_main():
    SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
    DEFAULT_CONFIG_PATH = os.path.abspath(os.path.join(SERVER_DIR, 'server_config.cfg'))

    parser = ArgumentParser(description="Test Sample Server")
    parser.add_argument('--config', required=False, default=DEFAULT_CONFIG_PATH,
                        help='Configuration file. Default: {0}'.format(DEFAULT_CONFIG_PATH))
    args = parser.parse_args()

    try:
        server_config = Config(args.config)
        _initialize_logging(server_config.log_path, server_config.log_level)
        _load_db(server_config.db_path)
        run(host=server_config.server_host, port=server_config.server_port, debug=True)
    except LoadConfigError:
        print('Config could not be loaded from {0}.\nCheck if the file exist in local machine.\n'.format(args.config))
        exit(1)
    except ConfigKeyError as e:
        print('Check that all necessary configuration keys are define in the config file.\n'
              'As an example of config file read the default one: {0}\n'.format(DEFAULT_CONFIG_PATH), str(e))
        logging.exception('Missing key definition in config file:\n{0}'.format(str(e)))
        exit(1)
    except DataBaseInstanceError as e:
        print('DB could not be loaded from the following file: {0}.\n'.format(server_config.db_path))
        logging.exception('Database could not be instanced:\n{0}'.format(str(e)))
        exit(1)


def _initialize_logging(log_path, log_level):
    logging.basicConfig(filename=log_path, format='%(asctime)s [%(levelname)s] - %(message)s')
    logging.getLogger().setLevel(log_level)
    logging.info('-------------- Starting server -------------- ')


def _load_db(db_path):
    logging.info('Loading DB from {0}'.format(db_path))
    DataBase.get_instance(db_path)


if __name__ == '__main__':
    server_main()
