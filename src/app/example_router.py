from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.utils import templates

example_router = APIRouter()


@example_router.get(
    "/",
    response_class=HTMLResponse,
)
async def index_page(
    request: Request,
) -> HTMLResponse:
    res: HTMLResponse = templates.TemplateResponse(
        request=request,
        name="example/index.html",
        context={},
    )
    return res
