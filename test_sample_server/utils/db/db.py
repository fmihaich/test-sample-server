from tinydb import TinyDB, Query

from models.user.user_attributes import UserAttr
from utils.db.db_errors import DataBaseInstanceError, DuplicateUserError, DataBaseInsertionError, DataBaseReadError


class DataBase(object):
    _instance = None

    @staticmethod
    def get_instance(*args):
        if DataBase._instance == None:
            DataBase(*args)
        return DataBase._instance

    def __init__(self, db_path):
        if DataBase._instance != None:
            raise DataBaseInstanceError("DB already loaded")
        try:
            self._db = TinyDB(db_path)
            DataBase._instance = self
        except Exception as e:
            raise DataBaseInstanceError('DB could not be loaded from "{0}":\n{1}'.format(db_path, str(e)))

    def insert_user(self, user):
        if self._db.search(Query()[UserAttr.ID] == user.id):
            raise DuplicateUserError('A user with ID "{0}" already exist'.format(user.id))

        try:
            self._db.insert(user.data)
        except Exception as e:
            raise DataBaseInsertionError("It was not possible insert the user:\n{0}".format(str(e)))

    def get_all_users(self):
        try:
            return self._db.all()
        except Exception as e:
            raise DataBaseReadError("It was not possible to get all users from database:\n{0}".format(str(e)))
