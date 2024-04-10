from typing import Any

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles

from app.auth_router import auth_router
from app.chat_router import chat_router
from app.utils import templates

security = HTTPBearer()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/chat")


@app.get("/")
def home() -> RedirectResponse:
    return RedirectResponse("/chat")


@app.get("/login", response_class=HTMLResponse)
def login(
    request: Request,
) -> HTMLResponse:
    res: HTMLResponse = templates.TemplateResponse(
        request=request,
        name="login.html",
    )

    return res


@app.get("/signup", response_class=HTMLResponse)
def signup(
    request: Request,
) -> HTMLResponse:
    res: HTMLResponse = templates.TemplateResponse(
        request=request,
        name="signup.html",
    )
    return res


@app.exception_handler(401)
async def custom_404_handler(_: Any, __: Any) -> RedirectResponse:
    return RedirectResponse("/login")
