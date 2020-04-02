import datetime

from models.user.user_attributes import UserAttr
from models.user.user_mgmt_errors import UserInsufficientData, UserInvalidDataType


class User(object):
    def __init__(self, user_data):
        self._data = user_data

        missing_mandatory_attr = self._get_missing_mandatory_attr()
        if missing_mandatory_attr:
            raise UserInsufficientData(
                'The following user attributes were not provided: {0}'.format(missing_mandatory_attr))

        if not self._check_valid_date():
            raise UserInvalidDataType('"{0}" shall have the following format: "m/d/y"'.format(UserAttr.BIRTHDAY))

    @property
    def id(self):
        return self._data[UserAttr.ID]

    @property
    def data(self):
        return self._data

    def _get_missing_mandatory_attr(self):
        mandatory_user_attr = UserAttr().get_all()
        missing_mandatory_attr = \
            [attr for attr in mandatory_user_attr if attr not in self._data or not self._data[attr]]
        return missing_mandatory_attr

    def _check_valid_date(self):
        try:
            datetime.datetime.strptime(self._data[UserAttr.BIRTHDAY], '%m/%d/%Y').date()
        except ValueError:
            return False
        return True
