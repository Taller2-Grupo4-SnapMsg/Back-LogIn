# user_search_tests.py
"""
This is a module for all the tests that are related to the user search.
"""
import pytest

from service.user_handler import UserHandler, MAX_AMMOUNT
from service.errors import MaxAmmountExceeded
from tests.utils import (
    remove_test_user_from_db,
    save_test_user_to_db,
    create_multiple_generic_users,
    remove_multiple_generic_users,
    USERNAME,
    EMAIL,
)

START = 0
AMMOUNT = 10

# We create the handler that will be used in all tests.
# Since the handler is stateless, we don't care if it's global.
handler = UserHandler()


def create_options_for_user_search(start, ammount, in_followers, email):
    """
    This function creates the options for the user search.
    """
    return {
        "start": start,
        "ammount": ammount,
        "in_followers": in_followers,
        "email": email,
    }


def test_search_for_ambiguous_term_and_only_get_ten():
    """
    This function tests that if we search a term that appears
    on both the name, username, and last name of the users, the users only
    appear once.
    """
    remove_test_user_from_db()

    create_multiple_generic_users(AMMOUNT)

    options = create_options_for_user_search(START, AMMOUNT, False, None)

    users = handler.search_for_users("Real", options)

    assert len(users) == AMMOUNT

    remove_multiple_generic_users(AMMOUNT)


def test_search_returns_a_list_of_users():
    """
    This function tests that if we search for a user, we get a list of users.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    options = create_options_for_user_search(START, AMMOUNT, False, None)

    users = handler.search_for_users(USERNAME, options)

    assert len(users) == 1
    assert users[0].email == EMAIL

    remove_test_user_from_db()


def test_search_for_a_name_partially():
    """
    This function tests that if we search for a user, we get a list of users.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    options = create_options_for_user_search(START, AMMOUNT, False, None)

    users = handler.search_for_users(USERNAME[0:3], options)

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

    options = create_options_for_user_search(START, AMMOUNT, False, None)

    users = handler.search_for_users(USERNAME[0:3], options)
    emails = [user.email for user in users]

    assert len(users) == AMMOUNT
    for i in range(0, AMMOUNT):
        assert EMAIL + str(i) in emails

    for i in range(0, AMMOUNT):
        remove_test_user_from_db(EMAIL + str(i))


def test_search_for_a_name_partially_multiple_users_with_start():
    """
    This function tests that if we search for a user, we get a list of users.
    """
    remove_test_user_from_db()

    create_multiple_generic_users(AMMOUNT)

    options = create_options_for_user_search(5, AMMOUNT, False, None)

    users = handler.search_for_users(USERNAME[0:3], options)

    assert len(users) == AMMOUNT - 5
    for i in range(0, AMMOUNT - 5):
        assert users[i].email == EMAIL + str(i + 5)

    remove_multiple_generic_users(AMMOUNT)


def test_search_for_users_and_there_is_none():
    """
    This function tests that if we search for a user that doesn't exist, we get an empty list.
    """
    remove_test_user_from_db()

    options = create_options_for_user_search(START, AMMOUNT, False, None)

    users = handler.search_for_users(USERNAME, options)

    assert len(users) == 0

    remove_test_user_from_db()


def test_search_for_users_and_there_is_none_with_start():
    """
    This function tests that if we search for a user that doesn't exist, we get an empty list.
    """
    remove_test_user_from_db()

    options = create_options_for_user_search(5, AMMOUNT, False, None)

    users = handler.search_for_users(USERNAME, options)

    assert len(users) == 0

    remove_test_user_from_db()


def test_search_for_user_that_doesnt_match_and_we_get_empty_list():
    """
    This function tests that if we search for a user that doesn't exist, we get an empty list.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    options = create_options_for_user_search(START, AMMOUNT, False, None)

    users = handler.search_for_users("not a user", options)

    assert len(users) == 0

    remove_test_user_from_db()


def test_search_for_user_surname_and_get_results():
    """
    This function tests that if we search by surname we get the correct results.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    options = create_options_for_user_search(START, AMMOUNT, False, None)

    users = handler.search_for_users("real_surname", options)

    assert len(users) == 1
    assert users[0].email == EMAIL

    remove_test_user_from_db()


def test_more_than_max_ammount_throws_exception():
    """
    This function tests that if we search for more than the max ammount of users,
    we get an exception.
    """
    pytest.raises(
        MaxAmmountExceeded, handler.search_for_users, "Real", START, MAX_AMMOUNT + 1
    )
