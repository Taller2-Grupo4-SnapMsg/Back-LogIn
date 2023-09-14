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


class DuplicatedPrimaryKey(Exception):
    """
    Exception raised when registering an user fails.
    """

    def __init__(self):
        super().__init__("Duplicated primary key")
