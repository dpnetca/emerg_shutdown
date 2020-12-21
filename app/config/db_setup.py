import mongoengine

from app.config import config


def register_connection():
    mongoengine.register_connection(
        alias="core",
        name="emerg_shutdown",
        username=config.mongo_db_user,
        password=config.mongo_db_pass,
        authentication_source="admin",
    )
