# admin_handler.py
"""
This module is for encapsulating all the admin related functions and logic.
"""
from repository.user_repository import (
    get_user_email,
    get_user_collection,
    make_admin as make_admin_repo,
    search_for_users_admins as search_for_users_admins_repo,
    remove_admin_status as remove_admin_repo,
    update_user_blocked_status as update_user_blocked_status_repo,
)
from service.user_handler import MAX_AMMOUNT
from service.errors import UserNotFound, MaxAmmountExceeded


class AdminHandler:
    """
    This class is for encapsulating all the admin related functions and logic.
    """

    def is_email_admin(self, email: str):
        """
        This function is used to check if a user is admin.
        """
        try:
            user = get_user_email(email)
            return user.admin
        except KeyError as error:
            raise UserNotFound() from error

    def make_admin(self, email: str):
        """
        This function is used to make a user an admin.
        """
        try:
            make_admin_repo(email)
        except KeyError as error:
            raise UserNotFound() from error

    def remove_admin_status(self, email: str):
        """
        This function is used to remove a user's admin status.
        """
        try:
            remove_admin_repo(email)
        except KeyError as error:
            raise UserNotFound() from error

    def get_all_users(self):
        """
        This function is used to get all users in the database.
        """
        return get_user_collection()

    def search_for_users_admins(self, username: str, start: int, ammount: int):
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
            raise MaxAmmountExceeded(
                "Ammount can't be greater than " + str(MAX_AMMOUNT)
            )
        return search_for_users_admins_repo(username, start, ammount)

    def change_blocked_status(self, email: str, blocked_status: bool):
        """
        This function is used to update the user in the database.

        :param email: The email of the user to update.
        :param blocked_status: The user's new blocked status.
        """
        try:
            update_user_blocked_status_repo(email, blocked_status)
        except KeyError as error:
            raise UserNotFound() from error
