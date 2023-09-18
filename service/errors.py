# errors.py

"""
This module is for exceptions that may be raised by the service layer.
"""


class UsernameAlreadyRegistered(Exception):
    """
    Exception raised when the user is already registered.
    """

    def __init__(self):
        super().__init__("Username already registered")


class EmailAlreadyRegistered(Exception):
    """
    Exception raised when the email is already registered.
    """

    def __init__(self):
        super().__init__("Email already registered")


class UserNotFound(Exception):
    """
    Exception raised when the user is not found on the database.
    """

    def __init__(self):
        super().__init__("User not found")


class PasswordDoesntMatch(Exception):
    """
    Exception raised when the password doesn't match.
    """

    def __init__(self):
        super().__init__("Password doesn't match")
