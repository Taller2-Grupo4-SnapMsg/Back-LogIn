# users.py
"""
This module is dedicated for all the users routes.
"""
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
    check_for_user_token,
    token_is_admin,
    generate_response,
    generate_response_list,
    generate_response_with_id,
    create_user_from_user_data,
    handle_user_registration,
    handle_user_login,
    handle_get_user_email,
)
from control.codes import (
    USER_NOT_FOUND,
    INCORRECT_CREDENTIALS,
    USER_NOT_ADMIN,
    BAD_REQUEST,
)

router = APIRouter(
    tags=["Users"],
)
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

# We create a global handler for the service layer.
# Since the handler is stateless, we don't care if it's global.
user_handler = UserHandler()


# Create a POST route
@router.post("/register", status_code=201)
def register_user(user_data: UserRegistration):
    """
    This function is the endpoint for user registration.
    """

    user = create_user_from_user_data(user_data)
    return handle_user_registration(user)


# Route to handle user login
@router.post("/login", status_code=200)
def login(user_data: UserLogIn):
    """
    This function is the endpoint for the mobile front to log in an already existing user

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    user = handle_get_user_email(user_data.email)
    if user.admin:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        )
    # user.password has the hashed_password.
    return handle_user_login(user_data.password, user.password, user_data.email)


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
        if user.admin:
            raise HTTPException(
                status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
            )
        token = auth_handler.encode_token(user.email)
        return {"message": "Login successful", "token": token}
    except InvalidIdTokenError as error:
        raise HTTPException(
            status_code=403, detail="Invalid Firebase ID token"
        ) from error


@router.get("/users/find", response_model=UserResponse)
def get_user(
    email: str = Query(None, title="Email", description="User email"),
    username: str = Query(None, title="Username", description="Username of the user"),
    token: str = Header(...),
):
    """
    This function retrieves a user by either email or username.

    :param email: The email of the user to get.
    :param username: The username of the user to get.
    :param token: Token used to verify the user.
    :return: User details or a 404 response.
    """
    # Checks the person requesting is a logged user:
    check_for_user_token(token)

    if email is None and username is None:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'email' or 'username' must be provided.",
        )

    if email:
        try:
            user = user_handler.get_user_email(email)
            user = generate_response(user)
            return user
        except UserNotFound as error:
            raise HTTPException(
                status_code=USER_NOT_FOUND, detail=str(error)
            ) from error

    if username:
        try:
            user = user_handler.get_user_username(username)
            user = generate_response(user)
            return user
        except UserNotFound as error:
            raise HTTPException(
                status_code=USER_NOT_FOUND, detail=str(error)
            ) from error
    # it never reachs here, but pylint...
    return {"message": "Something went wrong"}


@router.get("/users/interests")
def get_interests(token: str = Header(...)):
    """
    This function is for getting the user's interests

    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        return user_handler.get_user_interests(email)
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
        user_email = auth_handler.decode_token(
            token
        )  # auth_handler.auth_wrapper(token)
        user = user_handler.get_user_email(user_email)
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
        user_email = auth_handler.decode_token(
            token
        )  # auth_handler.auth_wrapper(token)
        user = user_handler.get_user_email(user_email)
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
    token: str = Header(...),
):
    """
    This function retrieves an user by token.

    :param token: The authentication token.
    :return: User details or a 401 response.
    """
    check_for_user_token(token)
    try:
        users = user_handler.search_for_users(query, int(offset), int(ammount))
    except MaxAmmountExceeded as error:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(error)) from error
    return generate_response_list(users)
