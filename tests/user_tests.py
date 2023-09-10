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

# from service.errors import UserAlreadyRegistered
# from service.errors import PasswordDoesntMatch

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


def test_user_can_login_after_register():
    """
    This function tests that the user is registered and can login.
    """
    remove_test_user_from_db()

    user = User(
        email="prueba",
        password="prueba",
        name="Real_name",
        surname="Real_surname",
        nickname=NICKNAME,
        date_of_birth="Real_date_of_birth",
        bio="Real_bio",
    )

    user.save()

    assert try_login("prueba", "prueba") == {"message": "Login successful"}

    remove_user_email("prueba")


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


# def test_user_already_registered():
#     """
#     This function tests the exception of user already registered.
#     """

#     remove_test_user_from_db()

#     save_test_user_to_db()

#     with pytest.raises(UserAlreadyRegistered) as error:
#         save_test_user_to_db()
#     assert str(error.value) == "User already registered"

#     remove_user_email(EMAIL)


# def test_wrong_password():
#     """
#     This function tests the exception of wrong password.
#     """

#     remove_test_user_from_db()

#     save_test_user_to_db()

#     with pytest.raises(PasswordDoesntMatch) as error:
#         try_login(EMAIL, "wrong_password")
#     assert str(error.value) == "Password doesn't match"

#     remove_user_email(EMAIL)


# def test_setters_work():
#     """
#     This function tests the setters.
#     """

#     remove_test_user_from_db()

#     user = User()

#     user.set_email(EMAIL)
#     user.set_password(PASSWORD)
#     user.set_name("Real_name")
#     user.set_surname("Real_surname")
#     user.set_nickname(NICKNAME)
#     user.set_date_of_birth("Real_date_of_birth")
#     user.set_bio("Real_bio")

#     assert user.email == EMAIL
#     assert user.password == PASSWORD
#     assert user.name == "Real_name"
#     assert user.surname == "Real_surname"
#     assert user.nickname == NICKNAME
#     assert user.date_of_birth == "Real_date_of_birth"
#     assert user.bio == "Real_bio"
