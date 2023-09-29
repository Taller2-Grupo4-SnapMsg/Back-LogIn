# user.py

"""
This module is for the service layer of the REST API for the login backend.
"""
from pydantic import BaseModel
from repository.user_repository import register_user
from repository.user_repository import update_user_password as update_user_password_repo
from repository.user_repository import update_user_bio as update_user_bio_repo
from repository.user_repository import update_user_name as update_user_name_repo
from repository.user_repository import (
    update_user_date_of_birth as update_user_date_of_birth_repo,
)
from repository.user_repository import (
    update_user_last_name as update_user_last_name_repo,
)
from repository.user_repository import update_user_avatar as update_user_avatar_repo
from repository.user_repository import get_user_email as get_user_repo
from repository.user_repository import remove_user
from repository.user_repository import get_user_collection
from repository.user_repository import get_user_username as get_user_username_repo
from repository.user_repository import make_admin as make_admin_repo
from repository.user_repository import remove_admin_status as remove_admin_repo
from repository.user_repository import create_follow as create_follow_repo
from repository.user_repository import get_followers as get_followers_db
from repository.user_repository import get_following as get_following_db
from repository.user_repository import (
    get_following_relations as get_following_relations_db,
)
from repository.user_repository import get_following_count as get_following_count_db
from repository.user_repository import get_followers_count as get_followers_count_db
from repository.user_repository import remove_follow as remove_follow_db
from repository.user_repository import update_user_location as update_user_location_repo
from repository.user_repository import (
    update_user_blocked_status as update_user_blocked_status_repo,
)
from repository.errors import UsernameAlreadyExists, EmailAlreadyExists
from repository.errors import RelationAlreadyExists
from service.errors import UserNotFound, PasswordDoesntMatch
from service.errors import UsernameAlreadyRegistered, EmailAlreadyRegistered
from service.errors import UserCantFollowItself, FollowingRelationAlreadyExists


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
            }
            register_user(self.email, self.password, self.username, data)
        except UsernameAlreadyExists as error:
            # if we had more errors we could do this and then default to a generic error:
            # if (error.response.detail) == "User already registered":
            raise UsernameAlreadyRegistered() from error
        except EmailAlreadyExists as error:
            raise EmailAlreadyRegistered() from error


# end class User


def try_login(email: str, password: str):
    """
    This function is used to login the user.

    :param email: The email of the user to login.
    :param password: The password of the user to login.
    """
    try:
        repo_user = get_user_repo(email)  # esto devuelve un usuario
        if repo_user.password != password:
            raise PasswordDoesntMatch()
    except KeyError as error:
        raise UserNotFound() from error
    return {"message": "Login successful"}


def change_password(email: str, new_password: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param new_passowrd: The user's new password.
    """
    try:
        update_user_password_repo(email, new_password)
    except KeyError as error:
        raise UserNotFound() from error


def change_bio(email: str, new_bio: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param new_bio: The user's new bio.
    """
    try:
        update_user_bio_repo(email, new_bio)
    except KeyError as error:
        raise UserNotFound() from error


def change_name(email: str, new_name: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param name: The user's new name.
    """
    try:
        update_user_name_repo(email, new_name)
    except KeyError as error:
        raise UserNotFound() from error


def change_date_of_birth(email: str, new_date_of_birth: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param new_date_of_birth: The user's new date of birth.
    """
    try:
        update_user_date_of_birth_repo(email, new_date_of_birth)
    except KeyError as error:
        raise UserNotFound() from error


def change_last_name(email: str, new_last_name: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param new_last_name: The user's new last name.
    """
    try:
        update_user_last_name_repo(email, new_last_name)
    except KeyError as error:
        raise UserNotFound() from error


def change_avatar(email: str, new_avatar: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param new_avatar: The user's new avatar.
    """
    try:
        update_user_avatar_repo(email, new_avatar)
    except KeyError as error:
        raise UserNotFound() from error


def change_location(email: str, new_location: str):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param new_location: The user's new location.
    """
    try:
        update_user_location_repo(email, new_location)
    except KeyError as error:
        raise UserNotFound() from error


def change_blocked_status(email: str, blocked_status: bool):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param blocked_status: The user's new blocked status.
    """
    try:
        update_user_blocked_status_repo(email, blocked_status)
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


def get_user_username(username: str):
    """
    This function is used to retrieve the user from the database.

    :param username: The username of the user to retrieve.
    :return: The user's information.
    """
    try:
        return get_user_username_repo(username)
    except KeyError as error:
        raise UserNotFound() from error


def remove_user_email(email: str):
    """
    This function is used to remove the user from the database.

    :param email: The email of the user to remove.
    """
    try:
        remove_user(email)
    except KeyError as error:
        raise UserNotFound() from error


def remove_user_username(username: str):
    """
    This function is used to remove the user from the database.

    :param username: The username of the user to remove.
    """
    try:
        user = get_user_username(username)
        remove_user(user.email)
    except KeyError as error:
        raise UserNotFound() from error


def get_all_users():
    """
    This function is used to retrieve all users from the database.
    """
    return get_user_collection()


def is_email_admin(email: str):
    """
    This function is used to check if a user is admin.
    """
    try:
        user = get_user_email(email)
        return user.admin
    except KeyError as error:
        raise UserNotFound() from error


def make_admin(email: str):
    """
    This function is used to make a user admin.
    """
    try:
        make_admin_repo(email)
    except KeyError as error:
        raise UserNotFound() from error


def remove_admin_status(email: str):
    """
    This function is used to remove admin status from a user.
    """
    try:
        remove_admin_repo(email)
    except KeyError as error:
        raise UserNotFound() from error


def create_follow(email: str, email_to_follow: str):
    """
    This function is used to create a follow relationship.
    """
    if email == email_to_follow:
        raise UserCantFollowItself()
    try:
        create_follow_repo(email, email_to_follow)
    except KeyError as error:
        raise UserNotFound() from error
    except RelationAlreadyExists as error:
        raise FollowingRelationAlreadyExists() from error


def get_all_followers(email: str):
    """
    This function is used to retrieve all username's followers from the database.
    """
    try:
        user = get_user_email(email)
        return get_followers_db(user.id)
    except KeyError as error:
        raise UserNotFound() from error


def get_all_following(email: str):
    """
    This function is used to retrieve all users following  username from the database.
    """
    try:
        user = get_user_email(email)
        return get_following_db(user.id)
    except KeyError as error:
        raise UserNotFound() from error


def get_all_following_relations():
    """
    This function is used to retrieve all follow relations from the database.
    """
    return get_following_relations_db()


def get_following_count(email: str):
    """
    This function is used to get email's following count from database.
    """
    try:
        user = get_user_email(email)
        return get_following_count_db(user.id)
    except KeyError as error:
        raise UserNotFound() from error


def get_followers_count(email: str):
    """
    This function is used to get email's followers count from database.
    """
    try:
        user = get_user_email(email)
        return get_followers_count_db(user.id)
    except KeyError as error:
        raise UserNotFound() from error


def remove_follow(email: str, email_to_unfollow: str):
    """
    This function is used to remove a follow relationship.
    """
    try:
        user = get_user_email(email)
        user_to_unfollow = get_user_email(email_to_unfollow)
        remove_follow_db(user.id, user_to_unfollow.id)
        return {"message": "Unfollow successful"}
    except KeyError as error:
        raise UserNotFound() from error
