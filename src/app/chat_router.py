from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse

from app import schemas
from app.db import models
from app.service import AppService
from app.utils import get_app_service, get_user, templates

chat_router = APIRouter()


@chat_router.get(
    "/",
    response_class=HTMLResponse,
)
async def chats_page(
    request: Request,
    app_service: AppService = Depends(get_app_service),
    user: models.User = Depends(get_user),
) -> HTMLResponse:
    chats = await app_service.get_all_chats(user)
    res: HTMLResponse = templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={"user": user, "chats": chats.all()},
    )
    return res


@chat_router.get(
    "/{chat_id}",
    response_class=HTMLResponse,
)
async def chat_page(
    chat_id: int,
    request: Request,
    app_service: AppService = Depends(get_app_service),
    user: models.User = Depends(get_user),
) -> HTMLResponse:
    chat = await app_service.get_chat_by_id(chat_id, user)

    chats = await app_service.get_all_chats(user)
    res: HTMLResponse = templates.TemplateResponse(
        request=request,
        name="chat-id.html",
        context={"user": user, "chat": chat, "chats": chats.all()},
    )
    return res


@chat_router.post(
    "/",
)
async def create_chat(
    data: schemas.CreateChat,
    response: Response,
    app_service: AppService = Depends(get_app_service),
    user: models.User = Depends(get_user),
) -> None:
    chat = await app_service.create_chat(user=user, data=data)
    response.headers["HX-Redirect"] = f"/chat/{chat.id}"


@chat_router.post(
    "/{chat_id}/add-message",
    response_class=HTMLResponse,
)
async def add_message(
    chat_id: int,
    data: schemas.AddMessage,
    response: Response,
    app_service: AppService = Depends(get_app_service),
    user: models.User = Depends(get_user),
) -> None:
    await app_service.add_message(user=user, data=data, chat_id=chat_id)
    response.headers["HX-Refresh"] = "true"


@chat_router.get(
    "/generate/{chat_id}",
)
async def generate(
    chat_id: int,
    app_service: AppService = Depends(get_app_service),
    user: models.User = Depends(get_user),
) -> EventSourceResponse:
    return EventSourceResponse(app_service.generate(chat_id))
