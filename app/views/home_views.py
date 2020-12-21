from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# build local router
router = APIRouter()

# define jinja2 template location
templates = Jinja2Templates(directory="app/templates")


# service index file - basic temproary place holder
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    data = {"message": "Hello World"}
    data["request"] = request
    return templates.TemplateResponse("home/index.j2", data)
