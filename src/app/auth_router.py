from fastapi import APIRouter, Depends, Response

from app import schemas
from app.service import AppService
from app.utils import get_app_service

auth_router = APIRouter()


@auth_router.post("/login")
async def login(
    response: Response,
    data: schemas.Login,
    app_service: AppService = Depends(get_app_service),
) -> None:
    """
    Endpoint for user login.

    Args:
        response (Response): The FastAPI Response object.
        data (schemas.Login): The login data provided by the user.
        app_service (AppService, optional): The AppService dependency. Defaults to Depends(get_app_service).
    """
    # TODO: Implement user login
    user = ...
    response.set_cookie(...)
    response.headers[...] = ...


@auth_router.post("/signup")
async def signup(
    response: Response,
    data: schemas.Signup,
    app_service: AppService = Depends(get_app_service),
) -> None:
    """
    Endpoint for user signup.

    Args:
        response (Response): The FastAPI Response object.
        data (schemas.Signup): The signup data provided by the user.
        app_service (AppService, optional): The AppService dependency. Defaults to Depends(get_app_service).
    """
    await app_service.create_user(data)
    response.headers["HX-Redirect"] = "/login"


@auth_router.get("/logout")
async def logout(
    response: Response,
) -> None:
    """
    Endpoint for user logout.

    Args:
        response (Response): The FastAPI Response object.
    """
    response.delete_cookie("python-htmx-workshop")
    response.headers["HX-Redirect"] = "/"
