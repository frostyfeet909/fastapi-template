import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

DIR__templates = os.path.abspath(os.path.join(__file__, "..", "templates"))
TEMPLATES = Jinja2Templates(directory=DIR__templates)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return TEMPLATES.TemplateResponse("home/v1.html.jinja", {"request": request})


@router.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return TEMPLATES.TemplateResponse("profile/v1.html.jinja", {"request": request})
