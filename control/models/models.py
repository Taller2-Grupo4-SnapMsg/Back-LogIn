# models.py
"""
This module is dedicated for all the pydantic models the API will use.
"""
from pydantic import BaseModel


class UserLogIn(BaseModel):
    """
    This class is a Pydantic model for the request body.
    """

    email: str
    password: str


# Define a Pydantic model for the request body
class UserRegistration(BaseModel):
    """
    This class is a Pydantic model for the request body.
    """

    password: str
    email: str
    name: str
    last_name: str
    username: str
    date_of_birth: str


class UserResponse(BaseModel):
    """
    This class is a Pydantic model for the response body.
    """

    email: str
    name: str
    last_name: str
    username: str
    date_of_birth: str
    bio: str
    avatar: str
    location: str
    blocked: bool

    # I disable it since it's a pydantic configuration
    # pylint: disable=too-few-public-methods
    class Config:
        """
        This is a pydantic configuration so I can cast
        orm_objects into pydantic models.
        """

        orm_mode = True
        from_attributes = True


class UserPostResponse(BaseModel):
    """
    This class is a Pydantic model for the response body.
    """

    id: int
    email: str
    name: str
    last_name: str
    username: str
    date_of_birth: str
    bio: str
    avatar: str
    location: str
    blocked: bool

    # I disable it since it's a pydantic configuration
    # pylint: disable=too-few-public-methods
    class Config:
        """
        This is a pydantic configuration so I can cast
        orm_objects into pydantic models.
        """

        orm_mode = True
        from_attributes = True
