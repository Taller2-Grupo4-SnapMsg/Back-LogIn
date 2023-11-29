# utils.py
"""
This module is for util functions in the controller layer.
"""
import datetime
from os import getenv
import pika
from fastapi import HTTPException
import requests
from control.utils.auth import auth_handler
from control.codes import (
    USER_ALREADY_REGISTERED,
    INCORRECT_CREDENTIALS,
    BLOCKED_USER,
    OK,
)
from control.models.models import (
    UserResponse,
    UserPostResponse,
    UserRegistration,
)
from control.utils.metrics import (
    RegistrationMetric,
    LoginMetric,
    RabbitMQManager,
)

from service.user import User
from service.user_handler import UserHandler
from service.admin_handler import AdminHandler
from service.errors import (
    UserNotFound,
    UsernameAlreadyRegistered,
    EmailAlreadyRegistered,
)


TIMEOUT = 5


admin_handler = AdminHandler()
user_handler = UserHandler()
rabbitmq_manager = RabbitMQManager()


# Check and get user from token
def check_and_get_user_from_token(token: str):
    """
    This function checks if the user is logged in.
    Used for everytime you need to check if the request
    is from a verified user, like in the following routes.
    """
    try:
        email = auth_handler.decode_token(token)
        user = user_handler.get_user_email(email)
        if user.blocked:
            raise HTTPException(status_code=BLOCKED_USER, detail="User is blocked.")
        return user
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
    headers_request = {
        "accept": "application/json",
        "content-type": "application/json",
        "token": token,
    }
    url = getenv("GATEWAY_URL") + "/admin/is_admin"
    response = requests.get(url, headers=headers_request, timeout=TIMEOUT)
    return response.status_code == OK


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
    user.set_blocked(False)
    return user


def handle_user_registration(user: User, registration_metric: RegistrationMetric):
    """
    This function handles user registration, it saves the user in the data base
    """
    try:
        user.save()
        token = auth_handler.encode_token(user.email)

        reg_json = (
            registration_metric.set_timestamp_finish(datetime.datetime.now())
            .set_user_email(user.email)
            .to_json()
        )
        push_metric(reg_json)

    except UsernameAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    except EmailAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    return {"message": "Registration successful", "token": token}


def handle_user_login(
    input_password: str,
    db_password: str,
    email: str,
    user: User,
    login_metric: LoginMetric,
):
    """
    This function handles user login, it checks if the password is correct
    and returns a token if it is.
    """
    login = (
        login_metric.set_timestamp_finish(datetime.datetime.now())
        .set_user_email(email)
        .set_success(False)
    )
    if not auth_handler.verify_password(input_password, db_password):
        login_json = login.to_json()
        push_metric(login_json)
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        )
    if user.blocked:
        login_json = login.to_json()
        push_metric(login_json)
        raise HTTPException(status_code=BLOCKED_USER, detail="User is blocked.")

    token = auth_handler.encode_token(email)

    login_json = login = login_metric.set_success(True).to_json()
    push_metric(login_json)
    return {"message": "Login successful", "token": token}


def handle_get_user_email(email: str, login_metric: LoginMetric):
    """
    This function handles getting a user from the data base.
    """
    try:
        return user_handler.get_user_email(email)
    except UserNotFound as error:
        login_json = (
            login_metric.set_timestamp_finish(datetime.datetime.now())
            .set_user_email(email)
            .set_success(False)
            .to_json()
        )
        push_metric(login_json)
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error


def push_metric(metric_json):
    """
    Wrapper for the publish into the rabbitmq_channel
    Checks if the connection is open, and sends the message
    if it is. If it isnt, reestablishes the connection
    and then sends the message.

    Also helps avoiding circular imports.
    """
    try:
        rabbitmq_manager.push_metric(metric_json)
    except (pika.exceptions.ChannelClosed, pika.exceptions.AMQPError):
        # Reestablish the RabbitMQ connection again
        rabbitmq_manager.push_metric(metric_json)
        # Add log
