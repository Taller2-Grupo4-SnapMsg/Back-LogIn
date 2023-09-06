# user_tests.py

"""
This is the test module.
"""
import pytest
from service.user import User

# from service.user import get_user_nickname
from service.user import remove_user_email
from service.user import get_user_email
from service.user import try_login
from service.errors import UserNotFound

EMAIL = "real_email@gmail.com"
NICKNAME = "real_nickname"
PASSWORD = "Real_password123"


def remove_test_user_from_db():
    """
    This function removes the test user from the database.
    """
    try:
        remove_user_email("real_email@gmail.com")
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
        nickname=NICKNAME,
        date_of_birth="Real_date_of_birth",
        bio="Real_bio",
    )

    user.save()


def test_user_login():
    """
    This function tests the user login.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    assert try_login(EMAIL, PASSWORD) == {"message": "Login successful"}

    remove_user_email(EMAIL)  # Que pasa si un test falla y esto no se ejecuta??


# This can't be tested without the database
# def test_user_get_nickname():
#     """
#     This function tests the user get by nickname.
#     """
#     remove_test_user_from_db()

#     save_test_user_to_db()

#     repo_user = get_user_nickname(NICKNAME)

#     assert repo_user["nickname"] == NICKNAME

#     remove_user_email(EMAIL)


def test_user_get_email():
    """
    This function tests the user get by email.
    """
    remove_test_user_from_db()

    save_test_user_to_db()

    repo_user = get_user_email(EMAIL)

    assert repo_user["email"] == EMAIL

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
