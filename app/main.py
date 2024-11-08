import json

from app.subapps import gpt
from fastapi import APIRouter, Depends, FastAPI, Request, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import (
    auth,
    businesses,
    departments,
    employee_functions,
    employees,
    insights,
    media,
    opa,
    roles,
    touchpoints,
    user_experiences,
    users,
    prediction,
)
from app.services.exceptions import NotFoundException, UserExperienceException

app = FastAPI()

origins = [
    "https://dev.d3f2mae5u40unb.amplifyapp.com",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(NotFoundException)
def handle_not_found(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"details": str(exc)}
    )


@app.exception_handler(UserExperienceException)
def handle_statemachine(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"details": str(exc)}
    )


@app.exception_handler(Exception)
def handle_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"details": str(exc)},
    )


with open("commit.json") as f:
    COMMIT = json.load(f)


@app.get("/")
def get_commit():
    return COMMIT


unauthenticated_routes = APIRouter()
authenticated_routes = APIRouter(dependencies=[Depends(auth.authorized_user)])

unauthenticated_routes.include_router(
    auth.router, prefix="/auth", tags=["Auth"]
)

unauthenticated_routes.include_router(
    users.router, prefix="/users", tags=["Users"]
)

unauthenticated_routes.include_router(
    user_experiences.router, prefix="/experiences", tags=["User Experiences"]
)

unauthenticated_routes.include_router(
    opa.router, prefix="/opa", tags=["Open Policy Agent"]
)


authenticated_routes.include_router(
    businesses.router,
    prefix="/businesses",
    tags=["Businesses"],
    dependencies=[Security(auth.authorized_user, scopes=["admin"])],
)


authenticated_routes.include_router(
    roles.router, prefix="/roles", tags=["Roles"]
)

authenticated_routes.include_router(
    departments.router, prefix="/departments", tags=["Departments"]
)

authenticated_routes.include_router(
    employees.router, prefix="/employees", tags=["Employees"]
)

authenticated_routes.include_router(
    employee_functions.router,
    prefix="/employee-functions",
    tags=["Employee functions"],
)

authenticated_routes.include_router(
    touchpoints.router, prefix="/touchpoints", tags=["Touchpoints"]
)

authenticated_routes.include_router(
    media.router, prefix="/media", tags=["Media"]
)

authenticated_routes.include_router(
    insights.router, prefix="/insights", tags=["Insights"]
)

unauthenticated_routes.include_router(
    prediction.router, prefix="/api/v1/prediction", tags=["Prediction"]
)


app.include_router(unauthenticated_routes)
app.include_router(authenticated_routes)

app.mount("/gpt", gpt.app)
