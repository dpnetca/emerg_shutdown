from typing import List

from fastapi import APIRouter

from app.services.cucm import cucm
from app.models import emerg_models


router = APIRouter(prefix="/emerg")


@router.get(
    "/", response_model=emerg_models.emerg_status, tags=["Emergency Status"]
)
def get_emergency_block_status():
    data = cucm.get_css_emerg_status()
    return data


@router.get(
    "/detail",
    response_model=List[emerg_models.css_status],
    tags=["Emergency Status"],
)
def get_emergency_block_details():
    data = cucm.get_css_emerg_status_all_detail()
    return data


@router.get(
    "/detail/{css}",
    response_model=emerg_models.css_status,
    tags=["Emergency Status"],
)
def get_emergency_block_details_for_css(css: str):
    data = cucm.get_css_emerg_status_detail(css)
    return data


@router.post("/lock", tags=["Emergency Status"])
def emerg_lockdown_all_pstn():
    data = cucm.emerg_lockdown_all()
    return data


@router.post("/unlock", tags=["Emergency Status"])
def emerg_remove_lockdown_all_pstn():
    data = cucm.emerg_remove_lockdown_all()
    return data
