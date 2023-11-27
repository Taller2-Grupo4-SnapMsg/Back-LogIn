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


class UserCantFollowItself(Exception):
    """
    Exception raised when the user tries to follow itself.
    """

    def __init__(self):
        super().__init__("User can't follow itself!")


class FollowingRelationAlreadyExists(Exception):
    """
    Exception raised when the user tries to follow another user that is already followed.
    """

    def __init__(self):
        super().__init__("Following relation already exists!")


class UserAlreadyHasBiometricToken(Exception):
    """
    Exception raised when you try to add a biometric token to a user that already has one.
    """

    def __init__(self):
        super().__init__("The user already has a biometric token set!")


class MaxAmmountExceeded(Exception):
    """
    Exception raised when searching for users and ammount is too big.
    """

    def __init__(self, message):
        super().__init__(message)
