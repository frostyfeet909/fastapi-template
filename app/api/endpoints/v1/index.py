from api.dependencies import TEMPLATES
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return TEMPLATES.TemplateResponse("base/v1.html.jinja", {"request": request})


@router.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return TEMPLATES.TemplateResponse("profile/v1.html.jinja", {"request": request})
