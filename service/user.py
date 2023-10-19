# user.py

"""
This module is for the service layer of the REST API for the login backend.
"""
from pydantic import BaseModel
from repository.user_repository import (
    register_user,
    update_user_password as update_user_password_repo,
    update_user_bio as update_user_bio_repo,
    update_user_name as update_user_name_repo,
    update_user_date_of_birth as update_user_date_of_birth_repo,
    update_user_last_name as update_user_last_name_repo,
    update_user_avatar as update_user_avatar_repo,
    get_user_email as get_user_repo,
    remove_user,
    get_user_collection,
    get_user_username as get_user_username_repo,
    make_admin as make_admin_repo,
    remove_admin_status as remove_admin_repo,
    update_user_location as update_user_location_repo,
    update_user_blocked_status as update_user_blocked_status_repo,
    set_user_interests as set_user_interests_repo,
    get_user_interests as get_user_interests_repo,
    search_for_users as search_for_users_repo,
    update_user_public_status as update_user_public_status_repo,
    search_for_users_admins as search_for_users_admins_repo,
)
from repository.errors import (
    UsernameAlreadyExists,
    EmailAlreadyExists,
)
from service.errors import (
    UsernameAlreadyRegistered,
    EmailAlreadyRegistered,
    UserNotFound,
    PasswordDoesntMatch,
    MaxAmmountExceeded,
)

MAX_AMMOUNT = 25


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


def change_public_status(email: str, public_status: bool):
    """
    This function is used to update the user in the database.

    :param email: The email of the user to update.
    :param public_status: The user's new public status.
    """
    try:
        update_user_public_status_repo(email, public_status)
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


def set_user_interests(email: str, interests: str):
    """
    This function is used to set the user's interests.

    :param email: The email of the user to update.
    :param interests: The user's interests in a string format like "Coooking,Cars,planes".
    """
    try:
        user = get_user_email(email)
        interests_list = interests.split(",")
        set_user_interests_repo(user.id, interests_list)
    except KeyError as error:
        raise UserNotFound() from error


def get_user_interests(email: str):
    """
    This function is used to get the user's interests.

    :param email: The email of the user to update.
    :return: The user's interest in a list
    """
    try:
        user = get_user_email(email)
        interests = get_user_interests_repo(user.id)
        return [interest.interest for interest in interests]
    except KeyError as error:
        raise UserNotFound() from error


def search_for_users(username: str, start: int, ammount: int):
    """
    This function is used to search for users.

    :param username: The username of the user to search for.
    :param start: The start of the search (offset).
    :param ammount: The ammount of users to return. if it's greater than
    MAX_AMMOUNT, it will be set to MAX_AMMOUNT. And if there is not enough users
    it will return everything it found.
    :return: A list of users.
    """
    if ammount > MAX_AMMOUNT:
        raise MaxAmmountExceeded("Ammount can't be greater than " + str(MAX_AMMOUNT))
    return search_for_users_repo(username, start, ammount)


def search_for_users_admins(username: str, start: int, ammount: int):
    """
    This function is used to search for users by the admins, the only
    difference with the other function, is that this one lists all the users
    while the other only lists users that are not admins.

    :param username: The username of the user to search for.
    :param start: The start of the search (offset).
    :param ammount: The ammount of users to return. if it's greater than
    MAX_AMMOUNT, it will be set to MAX_AMMOUNT. And if there is not enough users
    it will return everything it found.
    :return: A list of users.
    """
    # We set a max ammount so bad people can't overload the server
    if ammount > MAX_AMMOUNT:
        raise MaxAmmountExceeded("Ammount can't be greater than " + str(MAX_AMMOUNT))
    return search_for_users_admins_repo(username, start, ammount)
