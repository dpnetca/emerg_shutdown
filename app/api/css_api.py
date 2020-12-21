from typing import List

from fastapi import APIRouter

from app.services.cucm import cucm
from app.models import css_models


router = APIRouter(prefix="/css")


@router.get("/", response_model=List[css_models.css], tags=["css"])
def get_css_list():
    data = cucm.get_css_list()
    return data


@router.get("/{css_name}", response_model=css_models.css_detail, tags=["css"])
def get_css_details(css_name: str):
    data = cucm.get_css_detail(css_name)
    return data
