# controller.py

"""
This is the controller layer of the REST API for the user's backend.
"""
# Para permitir pegarle a la API desde localhost:
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from ddtrace import tracer, patch, config
from control.routers import followers, admins, users, users_put

patch(fastapi=True)

config.fastapi["request_span_name"] = "http.request"

tracer.configure(hostname="datadog_stats", port=8126)
tracer.trace("users-api", service="back-users")
tracer.set_tags({"env": "dev"})
tracer.set_tags({"service": "back-users"})

app = FastAPI(
    title="User's API", description="This is the API for the user's microservice."
)

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
