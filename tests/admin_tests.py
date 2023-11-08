# admin_tests.py

"""
This is the test module for admin related functions.
"""

import pytest
from service.admin_handler import AdminHandler
from service.user_handler import UserHandler
from service.errors import (
    UserNotFound,
)
from tests.utils import (
    remove_test_user_from_db,
    save_test_user_to_db,
    EMAIL,
)

START = 0
AMMOUNT = 10

# We create the handler that will be used in all tests.
# Since the handler is stateless, we don't care if it's global.
handler = AdminHandler()
user_handler = UserHandler()


def test_set_user_blocked_status():
    """
    This function tests that the user can be blocked.
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_blocked_status(EMAIL, True)

    assert user_handler.get_user_email(EMAIL).blocked is True

    remove_test_user_from_db()


def test_set_user_blocked_status_wrong_email():
    """
    This function tests the exception user not found
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_blocked_status("wrong_email", True)
    assert str(error.value) == "User not found"

    remove_test_user_from_db()


def test_unblock_an_user():
    """
    This function tests that the user can be unblocked.
    """
    remove_test_user_from_db()
    save_test_user_to_db()
    handler.change_blocked_status(EMAIL, True)
    assert user_handler.get_user_email(EMAIL).blocked is True
    handler.change_blocked_status(EMAIL, False)
    assert user_handler.get_user_email(EMAIL).blocked is False
    remove_test_user_from_db()
