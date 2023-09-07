# controler.py

"""
This is the controller layer of the REST API for the login backend.
"""

from fastapi import FastAPI, HTTPException

# Para permitir pegarle a la API desde localhost:
from fastapi.middleware.cors import CORSMiddleware
from service.user import User
from service.user import change_password as change_password_service
from service.user import get_user_email as get_user_service
from service.user import try_login
from service.user import remove_user_email
from service.errors import UserAlreadyRegistered, UserNotFound, PasswordDoesntMatch


app = FastAPI()

# Para permitir pegarle a la API desde localhost: (PREGUNTAR)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route to handle user registration
@app.post("/register/")
def register(email: str, password: str, name: str, last_name: str, nickname: str):
    """
    This function is a test function that mocks user registration.

    :param user: The user to register.
    :return: Status code with a JSON message.
    """
    user = User(email, password, name, last_name, nickname)

    try:
        user.save()
    except UserAlreadyRegistered as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {"message": "Registration successful"}


# Route to handle user login
@app.post("/login/")
def login(email: str, password: str):
    """
    This function is a test function that mocks user login.

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    try:
        try_login(email, password)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except PasswordDoesntMatch as error:
        raise HTTPException(status_code=401, detail=str(error)) from error
    return {"message": "Login successful"}


# Route to get user details
@app.get("/users/{email}/")
def get_user(email: str):
    """
    This function is a test function that mocks retrieving a user.

    :param email: The email of the user to get.
    :return: User details or a 404 response.
    """
    try:
        user = get_user_service(email)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return user


# Route to update user information
@app.put("/users/{email}/")
def change_password(email: str, new_password: str):
    """
    This function is a test function that mocks updating user information.

    :param email: The email of the user to update.
    :param update_info: New user information.
    :return: Status code with a JSON message.
    """
    try:
        change_password_service(email, new_password)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {"message": "User information updated"}


@app.delete("/users/{email}/")
def delete_user(email: str):
    """
    This function is a test function that mocks deleting a user.

    :param email: The email of the user to delete.
    :return: Status code with a JSON message.
    """
    try:
        remove_user_email(email)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {"message": "User deleted"}


@app.get("/ping")
def ping():
    """
    This function is a test function that mocks a ping.

    :return: Status code with a JSON message.
    """
    return {"message": "pong"}
