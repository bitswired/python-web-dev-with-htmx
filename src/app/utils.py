from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates

from app.db import AsyncSession, async_session, models
from app.service import AppService

security = HTTPBearer()

templates = Jinja2Templates(directory="templates")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_app_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[AppService, None]:
    yield AppService(session)


async def get_user(
    request: Request,
    app_service: AppService = Depends(get_app_service),
) -> AsyncGenerator[models.User, None]:
    cookie = request.cookies.get("python-htmx-workshop")

    if cookie is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    user = await app_service.get_user_by_id(int(cookie))
    print(user)

    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    yield user
