# admin_handler.py
"""
This module is for encapsulating all the admin related functions and logic.
"""
from repository.user_repository import (
    get_user_collection,
    update_user_blocked_status as update_user_blocked_status_repo,
)
from service.errors import UserNotFound


class AdminHandler:
    """
    This class is for encapsulating all the admin related functions and logic.
    """

    def get_all_users(self):
        """
        This function is used to get all users in the database.
        """
        return get_user_collection()

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
