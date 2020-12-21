from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.gadget_svc import gadget

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/helloWorld", include_in_schema=False)
def hello_world(request: Request):
    data = {"request": request, "content": {"message": "Coming Soon"}}
    return templates.TemplateResponse(
        "gadget/hello_world.xml", data, media_type="text/xml"
    )


@router.get("/", include_in_schema=False)
def gadget_status(request: Request):
    data = {"request": request, "content": gadget.get_status()}
    return templates.TemplateResponse(
        "gadget/gadget_status.xml", data, media_type="text/xml"
    )
