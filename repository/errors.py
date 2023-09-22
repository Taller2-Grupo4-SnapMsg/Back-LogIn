# errors.py

"""
This module is for exceptions that may be raised by the repository layer.
"""


class DatabaseTimeout(Exception):
    """
    Exception raised when the database times out.
    """

    def __init__(self):
        super().__init__("Database timeout")


class UsernameAlreadyExists(Exception):
    """
    Exception raised when registering an user fails.
    """

    def __init__(self):
        super().__init__("Username already exists")


class EmailAlreadyExists(Exception):
    """
    Exception raised when registering an user fails.
    """

    def __init__(self):
        super().__init__("Email already exists")


class RelationAlreadyExists(Exception):
    """
    Exception raised when creating a relation fails.
    """

    def __init__(self):
        super().__init__("Relation already exists")
