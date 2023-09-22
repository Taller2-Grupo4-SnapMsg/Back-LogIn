# user_tests.py

"""
This is the test module.
"""
import pytest
from service.user import User

# from service.user import get_user_username
from service.user import remove_user_email
from service.user import get_user_email
from service.user import try_login
from service.user import get_user_username
from service.user import make_admin
from service.user import remove_admin_status
from service.errors import UserNotFound
from service.errors import EmailAlreadyRegistered, UsernameAlreadyRegistered
from service.errors import PasswordDoesntMatch

EMAIL = "real_email@gmail.com"
USERNAME = "real_username"
PASSWORD = "Real_password123"


def remove_test_user_from_db():
    """
    This function removes the test user from the database.
    """
    try:
        remove_user_email(EMAIL)
    except UserNotFound:
        return


def save_test_user_to_db():
    """
    This function saves the test user to the database.
    """
    user = User(
        email=EMAIL,
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME,
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

    user.save()


def test_user_can_login_after_register():
    """
    This function tests that the user is registered and can login.
    """
    remove_test_user_from_db()

    user = User(
        email=EMAIL,
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username=USERNAME,
        date_of_birth="666 6 6",
        bio="Real_bio",
    )

    user.save()

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

    user = User(
        email="email_repe",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username="nick_no_repe",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

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

    user = User(
        email="email_no_repe",
        password=PASSWORD,
        name="Real_name",
        surname="Real_surname",
        username="username_repe",
        date_of_birth="666 6 6",
        bio="Real_bio",
        admin=False,
        avatar="image.png",
    )

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

    assert user.email == EMAIL
    assert user.password == PASSWORD
    assert user.name == "Real_name"
    assert user.surname == "Real_surname"
    assert user.username == USERNAME
    assert user.date_of_birth == "666 6 6"
    assert user.bio == "Real_bio"
    assert user.avatar == "image.png"
    assert user.admin is True


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
