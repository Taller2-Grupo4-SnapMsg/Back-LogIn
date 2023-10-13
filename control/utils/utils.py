# utils.py
"""
This module is for util functions in the controller layer.
"""
import datetime
from fastapi import HTTPException
from control.utils.auth import auth_handler
from control.codes import (
    USER_ALREADY_REGISTERED,
    INCORRECT_CREDENTIALS,
)
from control.models.models import (
    UserResponse,
    UserPostResponse,
    UserRegistration,
)
from service.user import User
from service.user import (
    get_user_email as get_user_service,
    is_email_admin,
)
from service.errors import (
    UserNotFound,
    UsernameAlreadyRegistered,
    EmailAlreadyRegistered,
)


def check_for_user_token(token: str):
    """
    This function checks if the user is logged in.
    Used for everytime you need to check if the request
    is from a verified user, like in the following routes.
    """
    try:
        email = auth_handler.decode_token(token)
        get_user_service(email)
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error


def generate_response(user):
    """
    This function casts the orm_object into a pydantic model.
    (from data base object to json)
    """
    return UserResponse(
        email=user.email,
        name=user.name,
        last_name=user.surname,
        username=user.username,
        date_of_birth=str(user.date_of_birth),
        bio=user.bio,
        avatar=user.avatar,
        location=user.location,
        blocked=user.blocked,
        is_public=user.is_public,
    )


def generate_response_with_id(user):
    """
    This function casts the orm_object into a pydantic model.
    (from data base object to json)
    """
    return UserPostResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        last_name=user.surname,
        username=user.username,
        date_of_birth=str(user.date_of_birth),
        bio=user.bio,
        avatar=user.avatar,
        location=user.location,
        blocked=user.blocked,
        is_public=user.is_public,
    )


def generate_response_list(users):
    """
    This function casts the list of users into a list of pydantic models.
    """
    response = []
    for user in users:
        response.append(generate_response(user))
    return response


def token_is_admin(token: str):
    """
    This function checks if the token given is an admin.
    """
    email = auth_handler.decode_token(token)
    try:
        return is_email_admin(email)
    # in theory, this should never happen, since the token is verified
    # We can't have a valid token that doesn't belong to a user
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error


def create_user_from_user_data(user_data: UserRegistration):
    """
    This function creates a user from the user data.
    """
    user = User()

    hashed_password = auth_handler.get_password_hash(user_data.password)
    user.set_password(hashed_password)

    user.set_email(user_data.email)
    user.set_name(user_data.name)
    user.set_surname(user_data.last_name)
    user.set_username(user_data.username)
    user.set_bio("")
    date_time = user_data.date_of_birth.split(" ")
    user.set_date_of_birth(
        datetime.datetime(int(date_time[0]), int(date_time[1]), int(date_time[2]))
    )
    user.set_admin(False)
    user.set_blocked(False)
    return user


def handle_user_registration(user: User):
    """
    This function handles user registration, it saves the user in the data base
    """
    try:
        user.save()
        token = auth_handler.encode_token(user.email)
    except UsernameAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    except EmailAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    return {"message": "Registration successful", "token": token}


def handle_user_login(input_password: str, db_password: str, email: str):
    """
    This function handles user login, it checks if the password is correct
    and returns a token if it is.
    """
    if not auth_handler.verify_password(input_password, db_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    token = auth_handler.encode_token(email)
    return {"message": "Login successful", "token": token}


def handle_get_user_email(email: str):
    """
    This function handles getting a user from the data base.
    """
    try:
        return get_user_service(email)
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
