from fastapi import APIRouter
from app.views import home_views, css_views, emerg_views

# build local router
router = APIRouter()

# add views to router
router.include_router(home_views.router)
router.include_router(css_views.router)
router.include_router(emerg_views.router)
