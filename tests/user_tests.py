# user_tests.py

"""
This is the test module.
"""
from datetime import datetime

import pytest
from service.user import User

from service.user import (
    get_user_email,
    get_user_username,
    remove_user_email,
    remove_user_username,
    try_login,
    make_admin,
    remove_admin_status,
    change_bio,
    change_avatar,
    change_name,
    change_date_of_birth,
    change_last_name,
    change_location,
    change_blocked_status,
    change_public_status,
)
from service.errors import (
    EmailAlreadyRegistered,
    UsernameAlreadyRegistered,
    PasswordDoesntMatch,
    UserNotFound,
)

EMAIL = "real_email@gmail.com"
USERNAME = "real_username"
PASSWORD = "Real_password123"


def create_generic_user(email=EMAIL, username=USERNAME, password=PASSWORD):
    """
    Function to create a generic user that is used on the tests
    """
    return User(
        email=email,
        password=password,
        name="Real_name",
        surname="Real_surname",
        username=username,
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
        location="Real_location",
        blocked=False,
    )


def remove_test_user_from_db(email=EMAIL):
    """
    This function removes the test user from the database.
    """
    try:
        remove_user_email(email)
    except UserNotFound:
        return


def save_test_user_to_db(email=EMAIL, username=USERNAME, password=PASSWORD):
    """
    This function saves the test user to the database.
    """
    user = create_generic_user(email, username, password)

    user.save()


def test_user_can_login_after_register():
    """
    This function tests that the user is registered and can login.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    assert try_login(EMAIL, PASSWORD) == {"message": "Login successful"}

    remove_user_email(EMAIL)


def test_user_get_username():
    """
    This function tests the user get by username.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    repo_user = get_user_username(USERNAME)

    assert repo_user.username == USERNAME

    remove_user_email(EMAIL)


def test_user_get_username_wrong_nick():
    """
    This function tries to get the user but the nick doesn't exist
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        get_user_username("wrong_nick")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_user_get_email():
    """
    This function tests the user get by email.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    repo_user = get_user_email(EMAIL)

    assert repo_user.email == EMAIL

    remove_user_email(EMAIL)


def test_remove_user():
    """
    This function tests the user remove.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    remove_user_email(EMAIL)

    with pytest.raises(UserNotFound) as error:
        get_user_email(EMAIL)
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

    remove_user_email("email_repe")


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

    remove_user_email("email_no_repe")


def test_wrong_password():
    """
    This function tests the exception of wrong password.
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(PasswordDoesntMatch) as error:
        try_login(EMAIL, "wrong_password")
    assert str(error.value) == "Password doesn't match"

    remove_user_email(EMAIL)


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
    user.set_admin(True)
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
    assert user.admin is True
    assert user.location == "Argentina"
    assert user.blocked is True


def test_user_login():
    """
    This function tests the user login.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    assert try_login(EMAIL, PASSWORD) == {"message": "Login successful"}

    remove_user_email(EMAIL)


def test_user_login_wrong_password():
    """
    This function tests the exception password doesn't match
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(PasswordDoesntMatch) as error:
        try_login(EMAIL, "wrong_password")
    assert str(error.value) == "Password doesn't match"

    remove_user_email(EMAIL)


def test_user_login_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        try_login("wrong_email", PASSWORD)
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_user_remove_by_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_user_email("wrong_email")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


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


def test_remove_user_by_username():
    """
    This function tests the remove user by username.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    remove_user_username(USERNAME)

    with pytest.raises(UserNotFound) as error:
        get_user_email(EMAIL)
    assert str(error.value) == "User not found"


def test_remove_user_by_username_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

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


def test_remove_user_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_bio():
    """
    This function tests the change user bio.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_bio(EMAIL, "new_bio")

    assert get_user_email(EMAIL).bio == "new_bio"

    remove_user_email(EMAIL)


def test_change_user_bio_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_bio("wrong_email", "new_bio")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_avatar():
    """
    This function tests the change user avatar.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_avatar(EMAIL, "new_avatar")

    assert get_user_email(EMAIL).avatar == "new_avatar"

    remove_user_email(EMAIL)


def test_change_user_avatar_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_avatar("wrong_email", "new_avatar")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_name():
    """
    This function tests the change user name.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_name(EMAIL, "new_name")

    assert get_user_email(EMAIL).name == "new_name"

    remove_user_email(EMAIL)


def test_change_user_name_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_name("wrong_email", "new_name")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_date_of_birth():
    """
    This function tests the change user date of birth.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_date_of_birth(EMAIL, "999 9 9")

    assert get_user_email(EMAIL).date_of_birth == datetime(999, 9, 9)

    remove_user_email(EMAIL)


def test_change_user_date_of_birth_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_date_of_birth("wrong_email", "999 9 9")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_change_user_last_name():
    """
    This function tests the change user last name.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_last_name(EMAIL, "new_last_name")

    assert get_user_email(EMAIL).surname == "new_last_name"

    remove_user_email(EMAIL)


def test_change_user_last_name_wrong_email():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_last_name("wrong_email", "new_last_name")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_remove_user_username_wrong_username():
    """
    This function tests the exception user not found
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        remove_user_username("wrong_username")
    assert str(error.value) == "User not found"

    remove_user_email(EMAIL)


def test_set_user_location():
    """
    This function tests that the user can be set a new location.
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    change_location(EMAIL, "new_location")

    assert get_user_email(EMAIL).location == "new_location"

    remove_test_user_from_db()


def test_set_user_location_wrong_email():
    """
    This function tests the exception user not found
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_location("wrong_email", "new_location")
    assert str(error.value) == "User not found"

    remove_test_user_from_db()


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


def test_set_profile_to_private():
    """
    This function tests that a user can set it's profile to private.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_public_status(EMAIL, True)

    assert get_user_email(EMAIL).is_public is True

    remove_test_user_from_db()


def test_set_profile_to_private_wrong_email():
    """
    This function tests the exception user not found
    """

    remove_test_user_from_db()

    save_test_user_to_db()

    with pytest.raises(UserNotFound) as error:
        change_public_status("wrong_email", True)
    assert str(error.value) == "User not found"

    remove_test_user_from_db()


def test_set_profile_to_private_and_then_public():
    """
    This function tests that a user can set it's profile to private and then to public.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    change_public_status(EMAIL, True)

    assert get_user_email(EMAIL).is_public is True

    change_public_status(EMAIL, False)

    assert get_user_email(EMAIL).is_public is False

    remove_test_user_from_db()
