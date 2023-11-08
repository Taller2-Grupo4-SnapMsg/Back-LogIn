# user_tests.py

"""
This is the test module.
"""
from datetime import datetime

import pytest
from service.user import User
from service.user_handler import UserHandler

from service.errors import (
    EmailAlreadyRegistered,
    UsernameAlreadyRegistered,
    PasswordDoesntMatch,
    UserNotFound,
)
from tests.utils import (
    remove_test_user_from_db,
    save_test_user_to_db,
    create_generic_user,
    EMAIL,
    USERNAME,
    PASSWORD,
)

# We create the handler that will be used in all tests.
# Since the handler is stateless, we don't care if it's global.
handler = UserHandler()


def test_user_can_login_after_register():
    """
    This function tests that the user is registered and can login.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    assert handler.try_login(EMAIL, PASSWORD) == {"message": "Login successful"}

    handler.remove_user_email(EMAIL)


def test_user_get_username():
    """
    This function tests the user get by username.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    repo_user = handler.get_user_username(USERNAME)

    assert repo_user.username == USERNAME

    handler.remove_user_email(EMAIL)


def test_user_get_username_wrong_nick():
    """
    This function tries to get the user but the nick doesn't exist
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.get_user_username("wrong_nick")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_user_get_email():
    """
    This function tests the user get by email.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    repo_user = handler.get_user_email(EMAIL)

    assert repo_user.email == EMAIL

    handler.remove_user_email(EMAIL)


def test_remove_user():
    """
    This function tests the user remove.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.remove_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        handler.get_user_email(EMAIL)
    assert str(error.value) == "User not found"


def test_user_already_registered_email():
    """
    This function tests the exception of user already registered (email).
    """

    remove_test_user_from_db()

    user = create_generic_user(username="username_no_repe", email="email_repe")

    user.save()
    user.username = "username_no_repe1"
    with pytest.raises(EmailAlreadyRegistered) as error:
        user.save()
    assert str(error.value) == "Email already registered"

    handler.remove_user_email("email_repe")


def test_user_already_registered_username():
    """
    This function tests the exception of user already registered (username).
    """

    remove_test_user_from_db()

    user = create_generic_user(username="username_repe", email="email_no_repe")

    user.save()
    user.email = "email_no_repe1"
    with pytest.raises(UsernameAlreadyRegistered) as error:
        user.save()
    assert str(error.value) == "Username already registered"

    handler.remove_user_email("email_no_repe")


def test_wrong_password():
    """
    This function tests the exception of wrong password.
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(PasswordDoesntMatch) as error:
        handler.try_login(EMAIL, "wrong_password")
    assert str(error.value) == "Password doesn't match"

    handler.remove_user_email(EMAIL)


def test_setters_work():
    """
    This function tests the setters.
    """

    remove_test_user_from_db()

    user = User()

    user.set_email(EMAIL)
    user.set_password(PASSWORD)
    user.set_name("Real_name")
    user.set_surname("Real_surname")
    user.set_username(USERNAME)
    user.set_date_of_birth("666 6 6")
    user.set_bio("Real_bio")
    user.set_avatar("image.png")
    user.set_location("Argentina")
    user.set_blocked(True)

    assert user.email == EMAIL
    assert user.password == PASSWORD
    assert user.name == "Real_name"
    assert user.surname == "Real_surname"
    assert user.username == USERNAME
    assert user.date_of_birth == "666 6 6"
    assert user.bio == "Real_bio"
    assert user.avatar == "image.png"
    assert user.location == "Argentina"
    assert user.blocked is True


def test_user_login():
    """
    This function tests the user login.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    assert handler.try_login(EMAIL, PASSWORD) == {"message": "Login successful"}

    handler.remove_user_email(EMAIL)


def test_user_login_wrong_password():
    """
    This function tests the exception password doesn't match
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(PasswordDoesntMatch) as error:
        handler.try_login(EMAIL, "wrong_password")
    assert str(error.value) == "Password doesn't match"

    handler.remove_user_email(EMAIL)


def test_user_login_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.try_login("wrong_email", PASSWORD)
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_user_remove_by_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.remove_user_email("wrong_email")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_remove_user_by_username():
    """
    This function tests the remove user by username.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.remove_user_username(USERNAME)

    with pytest.raises(UserNotFound) as error:
        handler.get_user_email(EMAIL)
    assert str(error.value) == "User not found"


def test_remove_user_by_username_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_remove_user_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_change_user_bio():
    """
    This function tests the change user bio.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_bio(EMAIL, "new_bio")

    assert handler.get_user_email(EMAIL).bio == "new_bio"

    handler.remove_user_email(EMAIL)


def test_update_user_password_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_password("wrong_email", "new_password")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_update_user_password():
    """
    This function tests the update user password.
    """
    remove_test_user_from_db()
    remove_test_user_from_db(EMAIL + "1")

    save_test_user_to_db()

    handler.change_password(EMAIL, "new_password")

    user = handler.get_user_email(EMAIL)

    assert user.password == "new_password"

    handler.remove_user_email(EMAIL)


def test_change_user_bio_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_bio("wrong_email", "new_bio")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_change_user_avatar():
    """
    This function tests the change user avatar.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_avatar(EMAIL, "new_avatar")

    assert handler.get_user_email(EMAIL).avatar == "new_avatar"

    handler.remove_user_email(EMAIL)


def test_change_user_avatar_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_avatar("wrong_email", "new_avatar")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_change_user_name():
    """
    This function tests the change user name.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_name(EMAIL, "new_name")

    assert handler.get_user_email(EMAIL).name == "new_name"

    handler.remove_user_email(EMAIL)


def test_change_user_name_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_name("wrong_email", "new_name")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_change_user_date_of_birth():
    """
    This function tests the change user date of birth.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_date_of_birth(EMAIL, "999 9 9")

    assert handler.get_user_email(EMAIL).date_of_birth == datetime(999, 9, 9)

    handler.remove_user_email(EMAIL)


def test_change_user_date_of_birth_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_date_of_birth("wrong_email", "999 9 9")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_change_user_last_name():
    """
    This function tests the change user last name.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_last_name(EMAIL, "new_last_name")

    assert handler.get_user_email(EMAIL).surname == "new_last_name"

    handler.remove_user_email(EMAIL)


def test_change_user_last_name_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_last_name("wrong_email", "new_last_name")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_remove_user_username_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

    handler.remove_user_email(EMAIL)


def test_set_user_location():
    """
    This function tests that the user can be set a new location.
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_location(EMAIL, "new_location")

    assert handler.get_user_email(EMAIL).location == "new_location"

    remove_test_user_from_db()


def test_set_user_location_wrong_email():
    """
    This function tests the exception user not found
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_location("wrong_email", "new_location")
    assert str(error.value) == "User not found"

    remove_test_user_from_db()


def test_set_profile_to_private():
    """
    This function tests that a user can set it's profile to private.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_public_status(EMAIL, True)

    assert handler.get_user_email(EMAIL).is_public is True

    remove_test_user_from_db()


def test_set_profile_to_private_wrong_email():
    """
    This function tests the exception user not found
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        handler.change_public_status("wrong_email", True)
    assert str(error.value) == "User not found"

    remove_test_user_from_db()


def test_set_profile_to_private_and_then_public():
    """
    This function tests that a user can set it's profile to private and then to public.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    handler.change_public_status(EMAIL, True)

    assert handler.get_user_email(EMAIL).is_public is True

    handler.change_public_status(EMAIL, False)

    assert handler.get_user_email(EMAIL).is_public is False

    remove_test_user_from_db()
