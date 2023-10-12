# user_search_tests.py
"""
This is a module for all the tests that are related to the user search.
"""
from service.user import (
    search_for_users,
)
from tests.user_tests import (
    remove_test_user_from_db,
    save_test_user_to_db,
    USERNAME,
    EMAIL,
)

START = 0
AMMOUNT = 10


def test_search_returns_a_list_of_users():
    """
    This function tests that if we search for a user, we get a list of users.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    users = search_for_users(USERNAME, START, AMMOUNT)

    assert len(users) == 1
    assert users[0].email == EMAIL

    remove_test_user_from_db()


def test_search_for_a_name_partially():
    """
    This function tests that if we search for a user, we get a list of users.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    users = search_for_users(USERNAME[0:3], START, AMMOUNT)

    assert len(users) == 1
    assert users[0].email == EMAIL

    remove_test_user_from_db()


def test_search_for_a_name_partially_multiple_users():
    """
    This function tests that if we search for a partially complete username,
    we get a list of all users that have that username.
    """
    remove_test_user_from_db()

    for i in range(0, AMMOUNT):
        save_test_user_to_db(email=EMAIL + str(i), username=USERNAME + str(i))

    users = search_for_users(USERNAME[0:3], START, AMMOUNT)

    assert len(users) == AMMOUNT
    for i in range(0, AMMOUNT):
        assert users[i].email == EMAIL + str(i)

    for i in range(0, AMMOUNT):
        remove_test_user_from_db(EMAIL + str(i))


def test_search_for_a_name_partially_multiple_users_with_start():
    """
    This function tests that if we search for a user, we get a list of users.
    """
    remove_test_user_from_db()

    for i in range(0, AMMOUNT):
        save_test_user_to_db(email=EMAIL + str(i), username=USERNAME + str(i))

    users = search_for_users(USERNAME[0:3], 5, AMMOUNT)

    assert len(users) == AMMOUNT - 5
    for i in range(0, AMMOUNT - 5):
        assert users[i].email == EMAIL + str(i + 5)

    for i in range(0, AMMOUNT):
        remove_test_user_from_db(EMAIL + str(i))


def test_search_for_users_and_there_is_none():
    """
    This function tests that if we search for a user that doesn't exist, we get an empty list.
    """
    remove_test_user_from_db()

    users = search_for_users(USERNAME, START, AMMOUNT)

    assert len(users) == 0

    remove_test_user_from_db()


def test_search_for_users_and_there_is_none_with_start():
    """
    This function tests that if we search for a user that doesn't exist, we get an empty list.
    """
    remove_test_user_from_db()

    users = search_for_users(USERNAME, 5, AMMOUNT)

    assert len(users) == 0

    remove_test_user_from_db()


def test_search_for_user_that_doesnt_match_and_we_get_empty_list():
    """
    This function tests that if we search for a user that doesn't exist, we get an empty list.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    users = search_for_users("not a user", START, AMMOUNT)

    assert len(users) == 0

    remove_test_user_from_db()
