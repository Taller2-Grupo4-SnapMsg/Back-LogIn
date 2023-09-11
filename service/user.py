# user.py

"""
This module is for the service layer of the REST API for the login backend.
"""

from pydantic import BaseModel
from repository.user_repository import register_user
from repository.user_repository import update_user as update_user_repo
from repository.user_repository import get_user_email as get_user_repo
from repository.user_repository import remove_user
from repository.user_repository import get_user_collection
from repository.user_repository import get_user_nickname as get_user_nickname_repo
from service.errors import UserAlreadyRegistered, UserNotFound, PasswordDoesntMatch
import requests


# Pydantic model for users
class User(BaseModel):
    """
    This class is used to represent a user.
    """

    email: str = ""
    password: str = ""
    name: str = ""
    surname: str = ""
    nickname: str = ""
    date_of_birth: str = ""
    bio: str = ""

    def set_email(self, email):
        """
        This function is used to set the user's email.
        """
        self.email = email

    def set_password(self, password):
        """
        This function is used to set the user's password.
        """
        self.password = password

    def set_name(self, name):
        """
        This function is used to set the user's name.
        """
        self.name = name

    def set_surname(self, surname):
        """
        This function is used to set the user's surname.
        """
        self.surname = surname

    def set_nickname(self, nickname):
        """
        This function is used to set the user's nickname.
        """
        self.nickname = nickname

    def set_date_of_birth(self, date_of_birth):
        """
        This function is used to set the user's date of birth.
        """
        self.date_of_birth = date_of_birth

    def set_bio(self, bio):
        """
        This function is used to set the user's bio.
        """
        self.bio = bio

    def save(self):
        """
        This function is used to save the user to the database.
        """
        try:
            data = {
                "name": self.name,
                "surname": self.surname,
                "date_of_birth": self.date_of_birth,
                "bio": self.bio,
            }  # Thanks pylint
            register_user(self.email, self.password, self.nickname, data)
        except requests.RequestException as error:
            # if we had more errors we could do this and then default to a generic error:
            # if (error.response.detail) == "User already registered":
            raise UserAlreadyRegistered() from error

    def login(self):
        """
        This function is used to login the user.
        """
        try:
            repo_user = get_user_repo(self.email)  # esto devuelve un usuario
            if repo_user["password"] != self.password:
                raise PasswordDoesntMatch()
        except KeyError as error:
            raise UserNotFound() from error
        return {"message": "Login successful"}


# end class User


def try_login(email: str, password: str):
    """
    This function is used to login the user.

    :param email: The email of the user to login.
    :param password: The password of the user to login.
    """
    try:
        repo_user = get_user_repo(email)  # esto devuelve un usuario
        if repo_user["password"] != password:
            raise PasswordDoesntMatch()
    except KeyError as error:
        raise UserNotFound() from error
    return {"message": "Login successful"}


def change_password(email: str, new_password: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param user: The user's new information.
    """
    try:
        update_user_repo(email, new_password)
    except KeyError as error:
        raise UserNotFound() from error


def get_user_email(email: str):
    """
    This function is used to retrieve the user from the database.

    :param email: The email of the user to retrieve.
    :return: The user's information.
    """
    try:
        return get_user_repo(email)
    except KeyError as error:
        raise UserNotFound() from error


def get_user_nickname(nickname: str):
    """
    This function is used to retrieve the user from the database.

    :param email: The email of the user to retrieve.
    :return: The user's information.
    """
    try:
        return get_user_nickname_repo(nickname)
    except KeyError as error:
        raise UserNotFound() from error


def remove_user_email(email: str):
    """
    This function is used to remove the user from the database.

    :param email: The email of the user to remove.
    """
    try:
        user = get_user_email(email)
        remove_user(user["email"])
    except KeyError as error:
        raise UserNotFound() from error


def remove_user_nickname(nickname: str):
    """
    This function is used to remove the user from the database.

    :param nickname: The nickname of the user to remove.
    """
    try:
        user = get_user_nickname(nickname)
        remove_user(user["email"])
    except KeyError as error:
        raise UserNotFound() from error


def get_all_users():
    """
    This function is used to retrieve all users from the database.
    """
    return get_user_collection()
