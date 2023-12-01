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
from control.utils.tracer import tracer
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
    push_metric,
)
from control.utils.metrics import (
    GOOGLE_ENTITY,
    BIOMETRICS_ENTITY,
    RegistrationMetric,
    LoginMetric,
)

from control.codes import (
    USER_NOT_FOUND,
    INCORRECT_CREDENTIALS,
    USER_NOT_ADMIN,
    BAD_REQUEST,
    BLOCKED_USER,
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
@tracer.start_as_current_span("Register User - Users")
def register_user(user_data: UserRegistration):
    """
    This function is the endpoint for user registration.
    """
    registration_metric = RegistrationMetric(datetime.now())
    user = create_user_from_user_data(user_data)
    return handle_user_registration(user, registration_metric)


# Route to handle user login
@router.post("/login", status_code=200)
@tracer.start_as_current_span("Login User - Users")
def login(user_data: UserLogIn):
    """
    This function is the endpoint for the mobile front to log in an already existing user

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    login_metric = LoginMetric(datetime.now())
    user = handle_get_user_email(user_data.email, login_metric)
    # user.password has the hashed_password.
    return handle_user_login(
        user_data.password, user.password, user_data.email, user, login_metric
    )


@router.post("/login_with_google", status_code=200)
@tracer.start_as_current_span("Login User with Google - Users")
def login_with_google(firebase_id_token: str = Header(...)):
    """
    This function is the endpoint for logging in with a Google ID
    token using Firebase Authentication.

    :param firebase_id_token: Firebase ID token for Google authentication.
    :return: Status code with a JSON message.
    """
    try:
        login_metric = LoginMetric(datetime.now()).set_login_entity(GOOGLE_ENTITY)
        decoded_token = auth.verify_id_token(firebase_id_token)
        user = handle_get_user_email(decoded_token["email"], login_metric)
        if user.blocked:
            login_metric = (
                login_metric.set_timestamp_finish(datetime.now())
                .set_user_email(user.email)
                .set_success(False)
            ).to_json()
            push_metric(login_metric)
            raise HTTPException(status_code=BLOCKED_USER, detail="User is blocked.")

        token = auth_handler.encode_token(user.email)
        login_metric = (
            login_metric.set_timestamp_finish(datetime.now())
            .set_user_email(user.email)
            .set_success(True)
        ).to_json()
        push_metric(login_metric)
        return {"message": "Login successful", "token": token}
    except InvalidIdTokenError as error:
        login_metric = (
            login_metric.set_timestamp_finish(datetime.now())
            .set_user_email(
                firebase_id_token  # No me gusta, preguntarle al prof después
            )
            .set_success(False)
        ).to_json()
        push_metric(login_metric)
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Invalid Firebase ID token"
        ) from error


@router.get("/users/interests")
@tracer.start_as_current_span("Get User Interests - Users")
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
@tracer.start_as_current_span("Delete User - Users")
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
@tracer.start_as_current_span("Get User by Token - Users")
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
@tracer.start_as_current_span("Get User by Token with ID - Users")
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
@tracer.start_as_current_span("Search User - Users")
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


@router.post("/user/biometric_token")
@tracer.start_as_current_span("Add Biometric Token - Users")
def add_biometric_token(token: str = Header(...)):
    """
    This function is used to add a biometric token to the user.
    """
    try:
        user = check_and_get_user_from_token(token)
        biometric_token = auth_handler.create_biometric_token()
        user_handler.add_biometric_token(user.email, biometric_token)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "Biometric token added", "biometric_token": biometric_token}


@router.delete("/user/delete_biometric_token")
@tracer.start_as_current_span("Delete Biometric Token - Users")
def delete_biometric_token(
    token: str = Header(...), biometric_token: str = Header(...)
):
    """
    This function is used to add a biometric token to the user.
    """
    try:
        user = check_and_get_user_from_token(token)
        user_handler.remove_biometric_token(user.id, biometric_token)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "Biometric token deleted"}


@router.post("/login_with_biometrics")
@tracer.start_as_current_span("Login with Biometric Token - Users")
def login_with_biometrics(biometric_token: str = Header(...)):
    """
    This function is used to verify a biometric token of the user.
    """
    try:
        login_metric = LoginMetric(datetime.now()).set_login_entity(BIOMETRICS_ENTITY)
        user = user_handler.verify_biometric_token(biometric_token)
        token = auth_handler.encode_token(user.email)
        login_metric = (
            login_metric.set_timestamp_finish(datetime.now())
            .set_success(True)
            .set_user_email(user.email)
        )
        push_metric(login_metric.to_json())
        return {"message": "Login successful", "token": token}
    except UserNotFound as error:
        login_metric = (
            login_metric.set_timestamp_finish(datetime.now())
            .set_success(False)
            .set_user_email(biometric_token)
        )
        push_metric(login_metric.to_json())
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
