# users.py
"""
This module is dedicated for all the users routes.
"""
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.auth import InvalidIdTokenError

from fastapi import (
    APIRouter,
    Header,
    HTTPException,
    Query,
)
from service.user_handler import UserHandler
from service.errors import UserNotFound, MaxAmmountExceeded

from control.models.models import (
    UserLogIn,
    UserRegistration,
    UserResponse,
    UserPostResponse,
)
from control.utils.auth import auth_handler
from control.utils.utils import (
    token_is_admin,
    generate_response,
    generate_response_list,
    generate_response_with_id,
    create_user_from_user_data,
    handle_user_registration,
    handle_user_login,
    handle_get_user_email,
    check_and_get_user_from_token,
)
from control.codes import (
    USER_NOT_FOUND,
    INCORRECT_CREDENTIALS,
    USER_NOT_ADMIN,
    BAD_REQUEST,
    BLOCKED_USER,
)

from control.utils.metrics import (
    RegistrationMetric,
    # , LoginMetric,GeoZoneMetric
)


router = APIRouter(
    tags=["Users"],
)
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred, {"storageBucket": "snapmsg-a9735.appspot.com"})

# We create a global handler for the service layer.
# Since the handler is stateless, we don't care if it's global.
user_handler = UserHandler()


# Create a POST route
@router.post("/register", status_code=201)
def register_user(user_data: UserRegistration):
    """
    This function is the endpoint for user registration.
    """
    registration_metric = RegistrationMetric(datetime.now())
    user = create_user_from_user_data(user_data)
    return handle_user_registration(user, registration_metric)


# Route to handle user login
@router.post("/login", status_code=200)
def login(user_data: UserLogIn):
    """
    This function is the endpoint for the mobile front to log in an already existing user

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    user = handle_get_user_email(user_data.email)
    # user.password has the hashed_password.
    return handle_user_login(user_data.password, user.password, user_data.email, user)


@router.post("/login_with_google", status_code=200)
def login_with_google(firebase_id_token: str = Header(...)):
    """
    This function is the endpoint for logging in with a Google ID
    token using Firebase Authentication.

    :param firebase_id_token: Firebase ID token for Google authentication.
    :return: Status code with a JSON message.
    """
    try:
        decoded_token = auth.verify_id_token(firebase_id_token)
        user = handle_get_user_email(decoded_token["email"])
        if user.blocked:
            raise HTTPException(status_code=BLOCKED_USER, detail="User is blocked.")
        token = auth_handler.encode_token(user.email)
        return {"message": "Login successful", "token": token}
    except InvalidIdTokenError as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Invalid Firebase ID token"
        ) from error


@router.get("/users/interests")
def get_interests(token: str = Header(...)):
    """
    This function is for getting the user's interests

    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        user = check_and_get_user_from_token(token)
        return user_handler.get_user_interests(user.email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@router.delete("/users/{email}")
def delete_user(email: str, token: str = Header(...)):
    """
    This function is a test function that mocks deleting a user.

    :param email: The email of the user to delete.
    :param token: Token used to verify the user who is calling this is an admin
    or the same user as email.

    :return: Status code with a JSON message.
    """
    if token_is_admin(token) or email == auth_handler.decode_token(token):
        try:
            user_handler.remove_user_email(email)
        except UserNotFound as error:
            raise HTTPException(
                status_code=USER_NOT_FOUND, detail=str(error)
            ) from error
    else:
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Insufficient Permissions",
        )
    return {"message": "User deleted"}


@router.get("/get_user_by_token", response_model=UserResponse)
def get_user_by_token(token: str = Header(...)):
    """
    This function retrieves an user by token.

    :param token: The authentication token.
    :return: User details or a 401 response.
    """
    try:
        user = check_and_get_user_from_token(token)
        user = generate_response(user)
        return user
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail=str(error)
        ) from error
    except HTTPException as error:
        raise error


@router.get("/user", response_model=UserPostResponse)
def get_user_by_token_with_id(token: str = Header(...)):
    """
    This function retrieves an user by token.

    :param token: The authentication token.
    :return: User details or a 401 response.
    """
    try:
        user = check_and_get_user_from_token(token)
        user = generate_response_with_id(user)
        return user
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail=str(error)
        ) from error
    except HTTPException as error:
        raise error


@router.get("/user/search/{query}")
def search_users(
    query: str,
    offset=Query(0, title="offset", description="offset for pagination"),
    ammount=Query(10, title="ammount", description="max ammount of users to return"),
    in_followers: bool = Query(
        False, title="in_followers", description="search in followers"
    ),
    token: str = Header(...),
):
    """
    This function retrieves an user by token.

    :param token: The authentication token.
    :return: User details or a 401 response.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_search_options = {
            "start": int(offset),
            "ammount": int(ammount),
            "in_followers": in_followers,
            "email": user.email,
        }
        users = user_handler.search_for_users(query, user_search_options)
    except MaxAmmountExceeded as error:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(error)) from error
    return generate_response_list(users)
