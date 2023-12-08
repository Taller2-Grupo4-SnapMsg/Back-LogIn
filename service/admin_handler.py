# admin_handler.py
"""
This module is for encapsulating all the admin related functions and logic.
"""
from repository.user_repository import (
    get_user_collection,
    update_user_blocked_status as update_user_blocked_status_repo,
    manual_rollback,
)
from service.errors import UserNotFound
from service.errors import MaxAmmountExceeded
from service.user_handler import MAX_AMMOUNT


class AdminHandler:
    """
    This class is for encapsulating all the admin related functions and logic.
    """

    def get_all_users(self, start: int, ammount: int):
        """
        This function is used to get all users in the database in a paginated way.
        """
        if start < 0 or ammount < 0:
            raise ValueError("start and ammount must be positive")
        if ammount > MAX_AMMOUNT:
            raise MaxAmmountExceeded("ammount must be less than " + str(MAX_AMMOUNT))
        return get_user_collection(start, ammount)

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

    def rollback(self):
        """
        This function is used to rollback the session.
        """
        manual_rollback()
