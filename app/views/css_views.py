from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.cucm import cucm


router = APIRouter(prefix="/css")
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def css_list(request: Request):
    data = {"request": request, "content": cucm.get_css_list()}
    return templates.TemplateResponse("css/css_list.j2", data)


@router.get("/{css}", response_class=HTMLResponse, include_in_schema=False)
async def css_detail(css: str, request: Request):
    data = {"request": request, "content": cucm.get_css_detail(css)}
    return templates.TemplateResponse("css/css_detail.j2", data)
