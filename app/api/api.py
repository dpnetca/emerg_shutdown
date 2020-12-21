from fastapi import APIRouter

from app.api import css_api, emerg_api


router = APIRouter()
router.include_router(css_api.router)
router.include_router(emerg_api.router)
