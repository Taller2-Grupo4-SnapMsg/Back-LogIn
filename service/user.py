# user.py

"""
This module is for the service layer of the REST API for the login backend.
"""

from pydantic import BaseModel
from repository.user_repository import register
from repository.user_repository import update_user as update_user_repo
from repository.user_repository import get_user as get_user_repo
from service.errors import UserAlreadyRegistered, UserNotFound, PasswordDoesntMatch


# Pydantic model for users
class User(BaseModel):
    """
    This class is used to represent a user.
    """

    email: str
    password: str

    def save(self):
        """
        This function is used to save the user to the database.
        """
        try:
            register(self.email, self.password)
        except KeyError as error:
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


def update_user(email: str, new_password: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param user: The user's new information.
    """
    try:
        update_user_repo(email, new_password)
    except KeyError as error:
        raise UserNotFound() from error


def get_user(email: str):
    """
    This function is used to retrieve the user from the database.

    :param email: The email of the user to retrieve.
    :return: The user's information.
    """
    try:
        return get_user_repo(email)
    except KeyError as error:
        raise UserNotFound() from error
