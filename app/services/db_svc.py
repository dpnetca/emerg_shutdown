from app.models import db_models


def event_log(msg: str):
    event = db_models.EventLog()
    event.description = msg
    event.save()
