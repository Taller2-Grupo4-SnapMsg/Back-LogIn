# controler.py

"""
This is the controller layer of the REST API for the login backend.
"""

import random
from fastapi import FastAPI, HTTPException

# Para permitir pegarle a la API desde localhost:
from fastapi.middleware.cors import CORSMiddleware
from service.user import User
from service.user import update_user as update_user_service
from service.user import get_user as get_user_service
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


@app.get("/hello_world/")
def central_function():
    """
    This function is a test function.

    :return: Hello world.
    """
    return {"message": "Hello World"}


@app.get("/random/{limit}")
def get_random(limit: int):
    """
    This function is a test function that receives a parameter and returns
    a random number between 0 and the number given.

    :param limit: The limit of the random number.
    :return: Random number and limit.
    """
    random_number: int = random.randint(0, limit)
    return {"random": random_number, "limit": limit}


# Route to handle user registration
@app.post("/register/")
def register(user: User):
    """
    This function is a test function that mocks user registration.

    :param user: The user to register.
    :return: Status code with a JSON message.
    """
    print("This is the user email:")
    print(user.email)
    print("This is the user password:")
    print(user.password)
    try:
        user.save()
    except UserAlreadyRegistered as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {"message": "Registration successful"}


# Route to handle user login
@app.post("/login/")
def login(user: User):
    """
    This function is a test function that mocks user login.

    :param user: The user to login.
    :return: Status code with a JSON message.
    """
    try:
        user.login()
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
def update_user(email: str, new_password: str):
    """
    This function is a test function that mocks updating user information.

    :param email: The email of the user to update.
    :param update_info: New user information.
    :return: Status code with a JSON message.
    """
    try:
        update_user_service(email, new_password)
    except UserNotFound as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    return {"message": "User information updated"}


@app.get("/ping")
def ping():
    """
    This function is a test function that mocks a ping.

    :return: Status code with a JSON message.
    """
    return {"message": "pong"}
