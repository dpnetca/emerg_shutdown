from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.views import views
from app.api import api
from app.bot import bot
from app.gadget import gadget
from app.config import config, db_setup, test_environment
from app.services import db_svc


# initiate FastAPI
app = FastAPI()

# mount directory for static web files (css, images, binaries, etc)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# add routers
app.include_router(views.router, prefix="")
app.include_router(api.router, prefix="/api/v1")
app.include_router(bot.router, prefix="/bot")
app.include_router(gadget.router, prefix="/gadget")


@app.on_event("startup")
def startup_event():
    db_setup.register_connection()
    db_svc.event_log("APP Started")
    if config.env == "dev":
        test_environment.cucm_env.setup_cucm()
        db_svc.event_log("created CUCM test CSS/PT")
        test_environment.wt_bot.setup_webhooks()
        db_svc.event_log("created Webex Teams Webhooks")


@app.on_event("shutdown")
async def shutdown_event():
    db_svc.event_log("APP Shutdown")
    if config.env == "dev":
        test_environment.cucm_env.cleanup_cucm()
        db_svc.event_log("removed CUCM test CSS/PT")
        test_environment.wt_bot.cleanup_webhooks()
        db_svc.event_log("created Webex Teams Webhooks")
