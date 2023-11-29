# controller.py

"""
This is the controller layer of the REST API for the user's backend.
"""
import os
import uptrace
from opentelemetry import trace

# Para permitir pegarle a la API desde localhost:
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from control.routers import followers, admins, users, users_put

uptrace.configure_opentelemetry(
    dsn=os.environ.get("UPTRACE_DSN"),
    service_name="myservice",
    service_version="1.0.0",
    deployment_environment="production",
)

tracer = trace.get_tracer("app_or_package_name", "1.0.0")

with tracer.start_as_current_span("foo") as main:
    with tracer.start_as_current_span("bar"):
        print("Hello world from OpenTelemetry Python!")

    print("trace:", uptrace.trace_url(main))

uptrace.shutdown()

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
