# controller.py

"""
This is the controller layer of the REST API for the login backend.
"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

@app.get("/hello_world/")
def central_function():
    """
    this function is a test function.

    :return: hello world.
    """
    return {"message": "Hello World"}


@app.get('/random/{limit}')
def get_random(limit: int):
    """
    this function is a test function that recieves a parameter and returns
    a random number between 0 and the number given.
    :param limit: the limit of the random number.
    :return: hello world.
    """
    rn: int = random.randint(0, limit)
    return {'random': rn, 'limit': limit}

# Mock database to store user information
mock_db = {}

# Pydantic model for user registration
class UserRegistration(BaseModel):
    email: str
    password: str

# Pydantic model for updating user information
class UpdateUser(BaseModel):
    password: str

# Route to handle user registration
@app.post("/register/")
def register(user: UserRegistration):
    """
    this function is a test function that mocks a user registration.
    param: user: the user to register.
    :return: status code with a json message.
    """
    if user.email in mock_db:
        raise HTTPException(status_code=400, detail="User already registered")
    mock_db[user.email] = {
        "email": user.email,
        "password": user.password
    }
    return {"message": "Registration successful"}

# Route to get user details
@app.get("/users/{email}/")
def get_user(email: str):
    """
    this function is a test function that mocks a get of a user.
    param: user: the user to get.
    :return: status code with a json message.
    """    
    user = mock_db.get(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Route to update user information
@app.put("/users/{email}/")
def update_user(email: str, update_info: UpdateUser):
    """
    this function is a test function that mocks a update of a user.
    param: user: the user to update.
    :return: status code with a json message.
    """
    user = mock_db.get(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user["password"] = update_info.password
    return {"message": "User information updated"}

if __name__ == "__main__":
    uvicorn.run(app, port="8000", host="0.0.0.0")
