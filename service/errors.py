# errors.py

"""
This module is for exceptions that may be raised by the service layer.
"""


class UserAlreadyRegistered(Exception):
    """
    Exception raised when a user is already registered.
    """

    def __init__(self):
        super().__init__("User already registered")


class UserNotFound(Exception):
    """
    Exception raised when the user is not found on the database.
    """

    def __init__(self):
        super().__init__("User not found")
