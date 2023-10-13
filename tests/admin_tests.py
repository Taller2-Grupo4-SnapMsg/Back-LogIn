# admin_tests.py

"""
This is the test module for admin related functions.
"""

import pytest
from service.user import (
    make_admin,
    remove_admin_status,
    get_user_email,
    remove_user_email,
    search_for_users,
    search_for_users_admins,
    change_blocked_status,
)
from service.errors import (
    UserNotFound,
)
from tests.utils import (
    remove_test_user_from_db,
    save_test_user_to_db,
    create_multiple_generic_users,
    remove_multiple_generic_users,
    EMAIL,
    USERNAME,
)

START = 0
AMMOUNT = 10


def test_user_can_be_set_as_admin():
    """
    This function makes and admin, and then
    checks if the user is an admin.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    make_admin(EMAIL)

    assert get_user_email(EMAIL).admin is True

    remove_user_email(EMAIL)


def test_user_can_be_removed_of_its_admin_priviliges():
    """
    This function makes and admin, and then
    checks if the user is an admin.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    make_admin(EMAIL)

    assert get_user_email(EMAIL).admin is True

    remove_admin_status(EMAIL)

    assert get_user_email(EMAIL).admin is False

    remove_user_email(EMAIL)


def test_make_user_admin_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        make_admin("wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_admin_doesnt_appear_on_user_search():
    """
    This function tests that if we search for an admin with the
    search function of the users, we don't find it.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    make_admin(EMAIL)

    assert get_user_email(EMAIL).admin is True

    users = search_for_users(USERNAME, START, AMMOUNT)

    assert len(users) == 0

    remove_test_user_from_db()


def test_remove_admin_priviliges_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_admin_status("wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_admin_appears_when_using_search_with_admin():
    """
    This function tests that if we search for an admin with the
    search function of the users, we don't find it.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    make_admin(EMAIL)

    assert get_user_email(EMAIL).admin is True

    users = search_for_users_admins(USERNAME, START, AMMOUNT)

    assert len(users) == 1
    assert users[0].email == EMAIL

    remove_test_user_from_db()


def test_multiple_admins_appear_when_searching_for_admins():
    """
    This tests the search function with multiple admins
    """
    remove_test_user_from_db()

    create_multiple_generic_users(AMMOUNT)

    for i in range(0, AMMOUNT):
        make_admin(EMAIL + str(i))

    users = search_for_users_admins(USERNAME, START, AMMOUNT)
    emails = [user.email for user in users]

    assert len(users) == AMMOUNT
    for i in range(0, AMMOUNT):
        assert EMAIL + str(i) in emails

    remove_multiple_generic_users(AMMOUNT)


def test_set_user_blocked_status():
    """
    This function tests that the user can be blocked.
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    change_blocked_status(EMAIL, True)

    assert get_user_email(EMAIL).blocked is True

    remove_test_user_from_db()


def test_set_user_blocked_status_wrong_email():
    """
    This function tests the exception user not found
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_blocked_status("wrong_email", True)
    assert str(error.value) == "User not found"

    remove_test_user_from_db()


def test_unblock_an_user():
    """
    This function tests that the user can be unblocked.
    """
    remove_test_user_from_db()
    save_test_user_to_db()
    change_blocked_status(EMAIL, True)
    assert get_user_email(EMAIL).blocked is True
    change_blocked_status(EMAIL, False)
    assert get_user_email(EMAIL).blocked is False
    remove_test_user_from_db()
