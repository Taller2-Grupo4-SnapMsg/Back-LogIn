# controler.py

"""
This is the controller layer of the REST API for the user's backend.
"""
# Para permitir pegarle a la API desde localhost:
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from control.routers import followers, admins, users, users_put

app = FastAPI()
origins = ["*"]
# All the routers are here:
app.include_router(admins.router)
app.include_router(followers.router)
app.include_router(users.router)
app.include_router(users_put.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
