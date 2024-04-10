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
    user = await app_service.login(data)
    response.set_cookie(key="python-htmx-workshop", value=user.id)
    response.headers["HX-Redirect"] = "/"


@auth_router.post("/signup")
async def signup(
    response: Response,
    data: schemas.Signup,
    app_service: AppService = Depends(get_app_service),
) -> None:
    await app_service.create_user(data)
    response.headers["HX-Redirect"] = "/login"


@auth_router.get("/logout")
async def logout(
    response: Response,
) -> None:
    response.delete_cookie("python-htmx-workshop")
    response.headers["HX-Redirect"] = "/"
