import pytest

from assertpy import assert_that

from models.user.user import User
from models.user.user_attributes import UserAttr
from models.user.user_mgmt_errors import UserInsufficientData, UserInvalidDataType


VALID_USER_DATA_SAMPLE = {
    UserAttr.ID: "testuser",
    UserAttr.NAME: "Test",
    UserAttr.SURNAME: "User",
    UserAttr.EMAIL: "test_user@gmail.com",
    UserAttr.BIRTHDAY: "01/11/2011",
    UserAttr.ADDRESS: "123 Some St"
}


class TestUser(object):
    user_data_sample = None

    def setup(self):
        self.user_data_sample = VALID_USER_DATA_SAMPLE.copy()

    @pytest.mark.parametrize("user_data", [
        VALID_USER_DATA_SAMPLE,
        {UserAttr.ID: "user1", UserAttr.NAME: "name1", UserAttr.SURNAME: "surname1", UserAttr.EMAIL: "user_1@gmail.com",
         UserAttr.BIRTHDAY: "01/01/2001", UserAttr.ADDRESS: "111 Some St", 'extra_attr': 'unused_value'}
    ])
    def test_user_is_correctly_created_with_all_correct_data(self, user_data):
        User(user_data)
        assert True, 'No exception shall be raised'

    @pytest.mark.parametrize(
        "missing_att",
        [UserAttr.ID, UserAttr.NAME, UserAttr.SURNAME, UserAttr.EMAIL, UserAttr.BIRTHDAY, UserAttr.ADDRESS])
    def test_user_creation_raises_insufficient_data_error_when_missing_some_mandatory_attribute(self, missing_att):
        del self.user_data_sample[missing_att]
        with pytest.raises(UserInsufficientData):
            User(self.user_data_sample)

    @pytest.mark.parametrize("attr, empty_value", [
        (UserAttr.ID, None),
        (UserAttr.NAME, ""),
        (UserAttr.SURNAME, None),
        (UserAttr.EMAIL, ""),
        (UserAttr.BIRTHDAY, None),
        (UserAttr.ADDRESS, "")
    ])
    def test_user_creation_raises_insufficient_data_error_when_mandatory_attribute_has_no_value(self, attr, empty_value):
        self.user_data_sample[attr] = empty_value
        with pytest.raises(UserInsufficientData):
            User(self.user_data_sample)

    @pytest.mark.parametrize("invalid_date", ["INVALID-DATE-FORMAT", "25/25/2005"])
    def test_user_creation_raises_invalid_data_error_when_birthday_attribute_is_incorrect(self, invalid_date):
        self.user_data_sample[UserAttr.BIRTHDAY] = invalid_date
        with pytest.raises(UserInvalidDataType):
            User(self.user_data_sample)

    def test_user_data_returns_the_data_used_for_its_construction(self):
        user = User(self.user_data_sample)
        assert_that(user.data).is_equal_to(self.user_data_sample)

    def test_user_data_returns_the_user_name_used_for_its_construction_as_id(self):
        user = User(self.user_data_sample)
        assert_that(user.id).is_equal_to(self.user_data_sample['username'])
