import json
import logging

from bottle import HTTPResponse

from models.user.user import User
from models.user.user_mgmt_errors import UserInsufficientData, UserInvalidDataType
from utils.db.db import DataBase
from utils.db.db_errors import DataBaseInstanceError, DuplicateUserError, DataBaseInsertionError, DataBaseReadError
from utils.http.http_status import HttpStatus


def add_user(request):
    try:
        user_data = json.loads(request.body.read())
    except Exception as e:
        logging.exception('Error loading json data from request:\n{0}'.format(e))
        return HTTPResponse(status=HttpStatus.BAD_REQUEST, body='Request content type shall be an application/json')

    try:
        user = User(user_data)
    except (UserInsufficientData, UserInvalidDataType) as e:
        logging.exception('Invalid user data:\n{0}'.format(e))
        return HTTPResponse(status=HttpStatus.BAD_REQUEST, body=str(e))

    try:
        db = DataBase.get_instance()
        db.insert_user(user)
    except (DataBaseInstanceError, DuplicateUserError, DataBaseInsertionError) as e:
        logging.exception('Error storing user data:\n{0}'.format(e))
        return HTTPResponse(status=HttpStatus.INTERNAL_ERROR, body=str(e))

    logging.info('User was correctly created')
    return HTTPResponse(status=HttpStatus.CREATED)


def get_all_users():
    try:
        db = DataBase.get_instance()
        users = db.get_all_users()
    except (DataBaseInstanceError, DataBaseReadError) as e:
        logging.exception('Error getting all stored users:\n'.format(e))
        return HTTPResponse(status=HttpStatus.INTERNAL_ERROR, body=str(e))

    return HTTPResponse(status=HttpStatus.OK, body=json.dumps(users), content_type='application/json')

