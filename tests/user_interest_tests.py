# user_interests_tests.py

"""
This is the test module that tests the interests feature of users.
"""
import pytest
from tests.user_tests import (
    remove_test_user_from_db,
    save_test_user_to_db,
    EMAIL,
)
from service.user import (
    set_user_interests,
    get_user_interests,
)
from service.errors import UserNotFound


def test_you_can_set_user_interests():
    """
    This function tests if you can set user interests.
    """

    remove_test_user_from_db()
    save_test_user_to_db()

    interests = "Cooking,Music,Sports"

    set_user_interests(EMAIL, interests)

    interests_list = get_user_interests(EMAIL)

    assert "Cooking" in interests_list
    assert "Music" in interests_list
    assert "Sports" in interests_list

    remove_test_user_from_db()


def test_set_user_interests_wrong_email():
    """
    This function tests the exception user not found
    """

    remove_test_user_from_db()
    save_test_user_to_db()

    interests = "Cooking,Music,Sports"

    with pytest.raises(UserNotFound) as error:
        set_user_interests("wrong_email", interests)
    assert str(error.value) == "User not found"

    remove_test_user_from_db()
