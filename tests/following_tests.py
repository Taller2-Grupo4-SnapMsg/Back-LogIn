# follow_tests.py

"""
This is the test module that tests the follow feature between users.
"""
import pytest

from service.follow_handler import FollowHandler
from service.user_handler import UserHandler

from service.errors import (
    FollowingRelationAlreadyExists,
    UserCantFollowItself,
    UserNotFound,
)

from tests.utils import (
    remove_test_user_from_db,
    save_test_user_to_db,
    EMAIL,
    USERNAME,
    create_generic_user,
)

# We create global handlers for the service layer.
# Since the handlers are stateless, we don't care if it's global.
handler = FollowHandler()
user_handler = UserHandler()


def test_user_can_follow_another_user():
    """
    This function tests that a user can follow another user.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = user_handler.get_user_email(EMAIL)

    handler.create_follow(user.email, user_to_be_followed.email)

    assert handler.get_following_count(user.email) == 1
    assert handler.get_followers_count(user_to_be_followed.email) == 1

    followers = handler.get_all_followers(user_to_be_followed.email)

    assert followers[0].username == user.username

    following = handler.get_all_following(user.email)

    assert following[0].username == user_to_be_followed.username

    handler.remove_follow(user.email, user_to_be_followed.email)
    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_user_cant_follow_the_same_user_twice():
    """
    This function tests that a user can't follow the same user twice.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = user_handler.get_user_email(EMAIL)

    handler.create_follow(user.email, user_to_be_followed.email)

    assert handler.get_following_count(user.email) == 1
    assert handler.get_followers_count(user_to_be_followed.email) == 1

    with pytest.raises(FollowingRelationAlreadyExists) as error:
        handler.create_follow(user.email, user_to_be_followed.email)
    assert str(error.value) == "Following relation already exists!"

    handler.remove_follow(user.email, user_to_be_followed.email)

    assert handler.get_following_count(user.email) == 0
    assert handler.get_followers_count(user_to_be_followed.email) == 0

    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_user_cant_follow_itself():
    """
    This function tests that a user can't follow itself.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user = user_handler.get_user_email(EMAIL)

    with pytest.raises(UserCantFollowItself) as error:
        handler.create_follow(user.email, user.email)
    assert str(error.value) == "User can't follow itself!"

    user_handler.remove_user_email(EMAIL)


def test_user_cant_follow_user_that_doesnt_exist():
    """
    This function tests that a user can't follow a user that doesn't exist.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user = user_handler.get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        handler.create_follow(user.email, "wrong_email")
    assert str(error.value) == "User not found"

    user_handler.remove_user_email(EMAIL)


def test_user_cant_be_followed_by_a_user_that_doesnt_exist():
    """
    This function tests that a user can't be followed by a user that doesn't exist.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user = user_handler.get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        handler.create_follow("wrong_email", user.email)
    assert str(error.value) == "User not found"

    user_handler.remove_user_email(EMAIL)


def test_get_following_count_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.get_following_count("wrong_username")
    assert str(error.value) == "User not found"

    user_handler.remove_user_email(EMAIL)


def test_remove_follow_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = user_handler.get_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        handler.remove_follow(user.email, "wrong_username")
    assert str(error.value) == "User not found"

    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_get_all_following_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = user_handler.get_user_email(EMAIL)

    handler.create_follow(user.email, user_to_be_followed.email)

    with pytest.raises(UserNotFound) as error:
        handler.get_all_following("wrong_username")
    assert str(error.value) == "User not found"

    handler.remove_follow(user.email, user_to_be_followed.email)
    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_get_all_followers_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    user_to_be_followed = create_generic_user(EMAIL + "1", USERNAME + "1")

    user_to_be_followed.save()

    user = user_handler.get_user_email(EMAIL)

    handler.create_follow(user.email, user_to_be_followed.email)

    with pytest.raises(UserNotFound) as error:
        handler.get_all_followers("wrong_username")
    assert str(error.value) == "User not found"

    handler.remove_follow(user.email, user_to_be_followed.email)
    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_is_follower_returns_false_if_not_following():
    """
    This function tests the handler.is_follower function.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()
    save_test_user_to_db(EMAIL + "1", USERNAME + "1")

    assert handler.is_follower(EMAIL, EMAIL + "1") is False

    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_is_follower_returns_true_if_following():
    """
    This function tests the handler.is_follower function when the user is following.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()
    save_test_user_to_db(EMAIL + "1", USERNAME + "1")

    user = user_handler.get_user_email(EMAIL)
    user_to_be_followed = user_handler.get_user_email(EMAIL + "1")

    handler.create_follow(user.email, user_to_be_followed.email)

    assert handler.is_follower(user_to_be_followed.email, user.email)

    handler.remove_follow(user.email, user_to_be_followed.email)
    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_is_follower_wrong_email():
    """
    This function tests the exception that is raised when a user is not found.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()
    save_test_user_to_db(EMAIL + "1", USERNAME + "1")

    with pytest.raises(UserNotFound) as error:
        handler.is_follower(EMAIL, "wrong_email")
    assert str(error.value) == "User not found"

    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_is_following_wrong_email():
    """
    This function tests the exception that is raised when a user is not found.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()
    save_test_user_to_db(EMAIL + "1", USERNAME + "1")

    with pytest.raises(UserNotFound) as error:
        handler.is_follower("wrong_email", EMAIL + "1")
    assert str(error.value) == "User not found"

    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_is_following_returns_false_if_not_following():
    """
    This function tests the is_following function.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()
    save_test_user_to_db(EMAIL + "1", USERNAME + "1")

    assert handler.is_follower(EMAIL, EMAIL + "1") is False

    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")


def test_is_following_returns_true_if_following():
    """
    This function tests the is_following function when the user is following.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()
    save_test_user_to_db(EMAIL + "1", USERNAME + "1")

    user = user_handler.get_user_email(EMAIL)
    user_to_be_followed = user_handler.get_user_email(EMAIL + "1")

    handler.create_follow(user.email, user_to_be_followed.email)

    assert handler.is_follower(user_to_be_followed.email, user.email)

    handler.remove_follow(user.email, user_to_be_followed.email)
    user_handler.remove_user_email(EMAIL)
    user_handler.remove_user_email(EMAIL + "1")
