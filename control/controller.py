# controler.py

"""
This is the controller layer of the REST API for the login backend.
"""
import datetime
from pydantic import BaseModel

# Para permitir pegarle a la API desde localhost:
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query
from fastapi import Header
from fastapi import status

from service.user import User
from service.user import (
    change_password as change_password_service,
    change_bio as change_bio_service,
    change_name as change_name_service,
    change_date_of_birth as change_date_of_birth_service,
    change_last_name as change_last_name_service,
    change_avatar as change_avatar_service,
    change_location as change_location_service,
    change_blocked_status as change_blocked_status_service,
    get_user_email as get_user_service,
    remove_user_email,
    get_all_users as get_all_users_service,
    get_user_username,
    make_admin as make_admin_service,
    remove_admin_status as remove_admin_service,
    create_follow as create_follow_service,
    get_all_following_relations as get_all_following_relations_service,
    get_all_followers,
    get_all_following,
    get_followers_count as get_followers_count_service,
    get_following_count as get_following_count_service,
    remove_follow as remove_follow_service,
    is_email_admin,
    set_user_interests as change_interests_service,
    is_following as is_following_service,
    get_user_interests as get_user_interests_service,
)
from service.errors import UserNotFound
from service.errors import UsernameAlreadyRegistered, EmailAlreadyRegistered
from service.errors import UserCantFollowItself, FollowingRelationAlreadyExists
from control.auth import AuthHandler

USER_ALREADY_REGISTERED = 409
USER_NOT_FOUND = 404
USER_NOT_ADMIN = 400
INCORRECT_CREDENTIALS = status.HTTP_401_UNAUTHORIZED
BLOCKED_USER = status.HTTP_403_FORBIDDEN

app = FastAPI()
auth_handler = AuthHandler()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    )


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
    )


def generate_response_list(users):
    """
    This function casts the list of users into a list of pydantic models.
    """
    response = []
    for user in users:
        response.append(generate_response(user))
    return response


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
        raise error


def token_is_admin(token: str):
    """
    This function checks if the token given is an admin.
    """
    email = auth_handler.decode_token(token)
    return is_email_admin(email)


# Create a POST route
@app.post("/register", status_code=201)
def register_user(user_data: UserRegistration):
    """
    This function is the endpoint for user registration.
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
    try:
        user.save()
        token = auth_handler.encode_token(user_data.email)
    except UsernameAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    except EmailAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    return {"message": "Registration successful", "token": token}


@app.post("/register_admin")
def register_admin(user_data: UserRegistration):
    """
    This function is the endpoint for admin registration.
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
    user.set_admin(True)
    user.set_blocked(False)
    try:
        user.save()
        token = auth_handler.encode_token(user_data.email)
    except UsernameAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    except EmailAlreadyRegistered as error:
        raise HTTPException(
            status_code=USER_ALREADY_REGISTERED, detail=str(error)
        ) from error
    return {"message": "Registration successful", "token": token}


class UserLogIn(BaseModel):
    """
    This class is a Pydantic model for the request body.
    """

    email: str
    password: str


# Route to handle user login
@app.post("/login", status_code=200)
def login(user_data: UserLogIn):
    """
    This function is the endpoint for the mobile front to log in an already existing user

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    try:
        user = get_user_service(user_data.email)
        # user.password has the hashed_password.
        if auth_handler.verify_password(user_data.password, user.password):
            if user.blocked:
                raise HTTPException(
                    status_code=BLOCKED_USER,
                    detail="Your account is blocked. "
                    + "If you think this is a mistake, contact an admin",
                )
            token = auth_handler.encode_token(user_data.email)
            return {"message": "Login successful", "token": token}

        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        )
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error


@app.post("/login_admin", status_code=200, response_model=dict)
def login_admin(user_data: UserLogIn):
    """
    This function is the endpoint for the web backoffice front to log in an already existing admin

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    try:
        user = get_user_service(user_data.email)
        if not user.admin:
            raise HTTPException(
                status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
            )
        if auth_handler.verify_password(user_data.password, user.password):
            token = auth_handler.encode_token(user_data.email)
            return {"message": "Login successful", "token": token}

        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        )
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error


@app.post("/follow")
def create_follow(email_following: str, token: str = Header(...)):
    """
    This function creates a following relation between the given users.

    :param token: Identifier of the user who wants to follow someone.
    :param email_following: Email of the user that is going to be followed.
    :return: Status code with a JSON message.
    """
    try:
        email_follower = auth_handler.decode_token(token)
        create_follow_service(email_follower, email_following)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    except UserCantFollowItself as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except FollowingRelationAlreadyExists as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"message": "Follow successful"}


@app.get("/followers/{email}")
def get_followers(email: str, token: str = Header(...)):
    """
    This function returns the users a username is followed by.

    :param email: Email of the user to get the followers of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    try:
        check_for_user_token(token)
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
    # Does the actual request:
    try:
        user_list = get_all_followers(email)
        return generate_response_list(user_list)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@app.get("/is_following/{email}")
def get_is_following(email_following: str, token: str = Header(...)):
    """
    This function returns if the user is following the given user.

    :param email: Email of the user to check if is following.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    try:
        email_follower = auth_handler.decode_token(token)
        check_for_user_token(token)
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
    try:
        is_following = is_following_service(email_follower, email_following)
        return is_following
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@app.get("/following/{email}")
def get_following(email: str, token: str = Header(...)):
    """
    This function returns the users a username is following.

    :param email: Email of the user to get the following of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    try:
        check_for_user_token(token)
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
    # Does the actual request:
    try:
        user_list = get_all_following(email)
        return generate_response_list(user_list)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@app.get("/follow/{email}/count")
def get_followers_count(email: str, token: str = Header(...)):
    """
    This function returns the number of followers of a username.

    :param email: Email of the user to get the followers count of.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    try:
        check_for_user_token(token)
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
    # Does the actual request:
    try:
        return get_followers_count_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@app.get("/following/{email}/count")
def get_following_count(email: str, token: str = Header(...)):
    """
    This function returns the number of users a email is following.

    :param email: Email of the user to get the following count of.
    :param token: Token used to verify you are requesting from a valid user.
    :return: Status code with a JSON message.
    """
    # Checks the person requesting is a logged user:
    try:
        check_for_user_token(token)
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
    # Does the actual request:
    try:
        return get_following_count_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@app.delete("/unfollow")
def unfollow(email_unfollowing: str, token: str = Header(...)):
    """
    This function deletes a following relation between the given users.

    :param token: Identifier of the user that is going to unfollow someone.
    :param username_following: Username of the user that is going to be unfollowed.
    :return: Status code with a JSON message.
    """
    try:
        email_follower = auth_handler.decode_token(token)
        return remove_follow_service(email_follower, email_unfollowing)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@app.get("/users/find", response_model=UserResponse)
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
    try:
        check_for_user_token(token)
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error

    if email is None and username is None:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'email' or 'username' must be provided.",
        )

    if email:
        try:
            user = get_user_service(email)
            user = generate_response(user)
            return user
        except UserNotFound as error:
            raise HTTPException(
                status_code=USER_NOT_FOUND, detail=str(error)
            ) from error

    if username:
        try:
            user = get_user_username(username)
            user = generate_response(user)
            return user
        except UserNotFound as error:
            raise HTTPException(
                status_code=USER_NOT_FOUND, detail=str(error)
            ) from error
    # it never reachs here, but pylint...
    return {"message": "Something went wrong"}


# Route to update user information
@app.put("/users/password")
def change_password(new_password: str, token: str = Header(...)):
    """
    This function is for changing the user's password

    :param email: The email of the user to update.
    :param new_password: User's new password.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        new_password = auth_handler.get_password_hash(new_password)
        change_password_service(email, new_password)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@app.put("/users/bio")
def change_bio(new_bio: str, token: str = Header(...)):
    """
    This function is for changing the user's bio

    :param new_bio: User's new bio.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_bio_service(email, new_bio)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@app.put("/users/avatar")
def change_avatar(new_avatar: str, token: str = Header(...)):
    """
    This function is for changing the user's avatar

    :param new_avatar: User's new avatar.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_avatar_service(email, new_avatar)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@app.put("/users/name")
def change_name(new_name: str, token: str = Header(...)):
    """
    This function is for changing the user's name

    :param new_name: User's new name.
    :param token: Token used to identify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_name_service(email, new_name)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@app.put("/users/date_of_birth")
def change_date_of_birth(new_date_of_birth: str, token: str = Header(...)):
    """
    This function is for changing the user's date_of_birth

    :param new_date_of_birth: User's new date_of_birth.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_date_of_birth_service(email, new_date_of_birth)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@app.put("/users/last_name")
def change_last_name(new_last_name: str, token: str = Header(...)):
    """
    This function is for changing the user's last_name

    :param new_last_name: User's new last_name.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_last_name_service(email, new_last_name)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@app.put("/users/location")
def change_location(new_location: str, token: str = Header(...)):
    """
    This function is for changing the user's location

    :param new_location: User's new location.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_location_service(email, new_location)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@app.put("/users/interests")
def change_interests(new_interests: str, token: str = Header(...)):
    """
    This function is for changing the user's interests

    :param new_interests: User's new interests.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        change_interests_service(email, new_interests)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": "User information updated"}


@app.get("/users/interests")
def get_interests(token: str = Header(...)):
    """
    This function is for getting the user's interests

    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        email = auth_handler.decode_token(token)
        return get_user_interests_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error


@app.put("/users/block/{email}")
def set_blocked_status(email: str, blocked: bool, token: str = Header(...)):
    """
    This function is for changing a user's blocked status.

    :param email: Email of the user to block.
    :param blocked: New blocked status.
    :param token: Token used to verify the user.
    :return: Status code with a JSON message.
    """
    try:
        admin_email = auth_handler.decode_token(token)
        if not is_email_admin(admin_email):
            raise HTTPException(
                status_code=USER_NOT_ADMIN,
                detail="Only administrators can block users",
            )
        change_blocked_status_service(email, blocked)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is now " + ("blocked" if blocked else "unblocked")}


# Route to making an admin
@app.put("/users/{email}/make_admin")
def make_admin(email: str, token: str = Header(...)):
    """
    This function changes the status of email to admin.

    :param email: The email of the user to update.
    :param token: Token used to verify the user who is calling this is an admin.
    :return: Status code with a JSON message.
    """
    if not token_is_admin(token):
        raise HTTPException(
            status_code=USER_NOT_ADMIN,
            detail="Only administrators can make other users administrators",
        )
    try:
        make_admin_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is now an admin"}


# Route to removing admin status
@app.put("/users/{email}/remove_admin")
def remove_admin_status(email: str, token: str = Header(...)):
    """
    This function is a test function that mocks updating user information.

    :param email: The email of the user to update.
    :param token: Token used to verify the user who is calling this is an admin.
    :return: Status code with a JSON message.
    """
    try:
        if not token_is_admin(token):
            raise HTTPException(
                status_code=USER_NOT_ADMIN,
                detail="Only administrators can remove other users from being administrators",
            )
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
    try:
        remove_admin_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=USER_NOT_FOUND, detail=str(error)) from error
    return {"message": email + " is no longer an admin"}


@app.delete("/users/{email}")
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
            remove_user_email(email)
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


@app.get(
    "/users",
    responses={
        200: {"model": UserResponse, "description": "All users"},
        400: {"description": "Only administrators can get all users"},
    },
)
def get_all_users(token: str = Header(...)):
    """
    This function is a functon that returns all of the users in the database.

    :param token: Token used to verify the user who is calling this is an admin.

    :return: JSON of all users.
    """
    try:
        if not token_is_admin(token):
            raise HTTPException(
                status_code=USER_NOT_ADMIN,
                detail="Only administrators can get all users",
            )
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
    user_list = get_all_users_service()
    return generate_response_list(user_list)


@app.get("/following")
def get_all_following_relations(token: str = Header(...)):
    """
    This function is a function that returns all of the following relations in the database.

    :param token: Token used to verify the user who is calling this is an admin.

    :return: JSON of all users.
    """
    try:
        if not token_is_admin(token):
            raise HTTPException(
                status_code=USER_NOT_ADMIN,
                detail="Only administrators can get all following relations",
            )
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error
    return get_all_following_relations_service()


@app.get("/get_user_by_token", response_model=UserResponse)
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
        user = get_user_service(user_email)
        user = generate_response(user)
        return user
    except HTTPException as error:
        raise error


@app.get("/admin/is_admin")
def validate_admin_token(token: str = Header(...)):
    """
    This function checks if a token is an admin or not.

    :param token: The authentication token.
    :return: User details or a 401 response.
    """
    try:
        return {"is_admin": token_is_admin(token)}
    except UserNotFound as error:
        raise HTTPException(
            status_code=INCORRECT_CREDENTIALS, detail="Incorrect credentials"
        ) from error


@app.get("/user", response_model=UserPostResponse)
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
        user = get_user_service(user_email)
        user = generate_response_with_id(user)
        return user
    except HTTPException as error:
        raise error
