# follow_tests.py

"""
This is the test module that tests the follow feature between users.
"""
import pytest

from service.user import create_follow
from service.user import get_following_count
from service.user import get_followers_count
from service.user import get_all_followers
from service.user import get_all_following
from service.user import remove_follow
from service.user import change_password
from service.user import remove_user_email
from service.user import get_user_email

from service.errors import FollowingRelationAlreadyExists
from service.errors import UserCantFollowItself
from service.errors import UserNotFound

from tests.user_tests import remove_test_user_from_db
from tests.user_tests import save_test_user_to_db
from tests.user_tests import EMAIL
from tests.user_tests import USERNAME
from tests.user_tests import create_generic_user


def test_user_can_follow_another_user():
    """
    This function tests that a user can follow another user.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    create_follow(user.email, user_to_be_followed.email)

    assert get_following_count(user.email) == 1
    assert get_followers_count(user_to_be_followed.email) == 1

    followers = get_all_followers(user_to_be_followed.email)

    assert followers[0].username == user.username

    following = get_all_following(user.email)

    assert following[0].username == user_to_be_followed.username

    remove_follow(user.email, user_to_be_followed.email)
    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_user_cant_follow_the_same_user_twice():
    """
    This function tests that a user can't follow the same user twice.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    create_follow(user.email, user_to_be_followed.email)

    assert get_following_count(user.email) == 1
    assert get_followers_count(user_to_be_followed.email) == 1

    with pytest.raises(FollowingRelationAlreadyExists) as error:
        create_follow(user.email, user_to_be_followed.email)
    assert str(error.value) == "Following relation already exists!"

    remove_follow(user.email, user_to_be_followed.email)

    assert get_following_count(user.email) == 0
    assert get_followers_count(user_to_be_followed.email) == 0

    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_user_cant_follow_itself():
    """
    This function tests that a user can't follow itself.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user = get_user_email(EMAIL)

    with pytest.raises(UserCantFollowItself) as error:
        create_follow(user.email, user.email)
    assert str(error.value) == "User can't follow itself!"

    remove_user_email(EMAIL)


def test_user_cant_follow_user_that_doesnt_exist():
    """
    This function tests that a user can't follow a user that doesn't exist.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user = get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        create_follow(user.email, "wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_user_cant_be_followed_by_a_user_that_doesnt_exist():
    """
    This function tests that a user can't be followed by a user that doesn't exist.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user = get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        create_follow("wrong_email", user.email)
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_update_user_password():
    """
    This function tests the update user password.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    change_password(EMAIL, "new_password")

    user = get_user_email(EMAIL)

    assert user.password == "new_password"

    remove_user_email(EMAIL)


def test_update_user_password_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_password("wrong_email", "new_password")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_get_following_count_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        get_following_count("wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_remove_follow_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        remove_follow(user.email, "wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_get_all_following_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    create_follow(user.email, user_to_be_followed.email)

    with pytest.raises(UserNotFound) as error:
        get_all_following("wrong_username")
    assert str(error.value) == "User not found"

    remove_follow(user.email, user_to_be_followed.email)
    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")


def test_get_all_followers_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = get_user_email(EMAIL)

    create_follow(user.email, user_to_be_followed.email)

    with pytest.raises(UserNotFound) as error:
        get_all_followers("wrong_username")
    assert str(error.value) == "User not found"

    remove_follow(user.email, user_to_be_followed.email)
    remove_user_email(EMAIL)
    remove_user_email(EMAIL + "1")
