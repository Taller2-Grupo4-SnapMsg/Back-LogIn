# user.py

"""
This module is for the service layer of the REST API for the login backend.
"""
from pydantic import BaseModel
from repository.user_repository import (
    register_user,
)
from repository.errors import (
    UsernameAlreadyExists,
    EmailAlreadyExists,
)
from service.errors import (
    UsernameAlreadyRegistered,
    EmailAlreadyRegistered,
)


# Pydantic model for users
# pylint: disable=too-many-instance-attributes
class User(BaseModel):
    """
    This class is used to represent a user.
    """

    email: str = ""
    password: str = ""
    name: str = ""
    surname: str = ""
    username: str = ""
    date_of_birth: str = ""
    bio: str = ""
    avatar: str = ""
    admin: bool = False
    location: str = ""
    blocked: bool = False
    is_public: bool = True

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

    def set_username(self, username):
        """
        This function is used to set the user's username.
        """
        self.username = username

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

    def set_avatar(self, avatar):
        """
        This function is used to set the user's avatar.
        """
        self.avatar = avatar

    def set_admin(self, admin):
        """
        This function is used to set the user's admin.
        """
        self.admin = admin

    def set_location(self, location):
        """
        This function is for saving the user's location.
        """
        self.location = location

    def set_blocked(self, blocked_status):
        """
        This function is for modifying the user's blocked status.
        """
        self.blocked = blocked_status

    def set_public(self, public_status):
        """
        This function is for modifying the user's public status.
        """
        self.is_public = public_status

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
                "avatar": self.avatar,
                "admin": self.admin,
                "location": "",  # At time of registration, location is empty
                "blocked": False,  # At time of registration, user is not blocked
                "is_public": True,  # At time of registration, user is public
            }
            register_user(self.email, self.password, self.username, data)
        except UsernameAlreadyExists as error:
            # if we had more errors we could do this and then default to a generic error:
            # if (error.response.detail) == "User already registered":
            raise UsernameAlreadyRegistered() from error
        except EmailAlreadyExists as error:
            raise EmailAlreadyRegistered() from error
