from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.cucm import cucm


# build local router
router = APIRouter(prefix="/emerg")

# define jinja2 template location
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def emerg_status(request: Request):
    data = {"request": request, "content": cucm.get_css_emerg_status()}
    return templates.TemplateResponse("emerg/emerg.j2", data)


@router.post("/", include_in_schema=False)
def emerg_toggle_status(state: str = Form(...)):
    # need some CSRF secutiy here...
    if state == "lock":
        pass
    elif state == "unlock":
        pass
    else:
        pass
    return RedirectResponse("/emerg/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/detail", response_class=HTMLResponse, include_in_schema=False)
def emerg_status_all_detail(request: Request):
    data = {
        "request": request,
        "content": cucm.get_css_emerg_status_all_detail(),
    }
    return templates.TemplateResponse("emerg/emerg_all_detail.j2", data)


@router.get(
    "/detail/{css}", response_class=HTMLResponse, include_in_schema=False
)
def emerg_status_detail(css, request: Request):
    data = {
        "request": request,
        "content": cucm.get_css_emerg_status_detail(css),
    }
    return templates.TemplateResponse("emerg/emerg_detail.j2", data)
