import mongoengine
from datetime import datetime


class User(mongoengine.Document):
    first_name = mongoengine.StringField(required=True)
    last_name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    uid = mongoengine.StringField(required=True)  # uuid?

    title = mongoengine.StringField(required=False)
    work_phone = mongoengine.StringField(required=False)
    cell_phone = mongoengine.StringField(required=False)

    webex_id = mongoengine.StringField(required=False)
    role = mongoengine.StringField(default="NoAccess")

    meta = {"db_alias": "core", "collection": "users"}


class EventLog(mongoengine.Document):
    # e_id = mongoengine.SequenceField(required=True)
    date = mongoengine.DateTimeField(default=datetime.now)
    description = mongoengine.StringField(required=True)

    meta = {"db_alias": "core", "collection": "eventLogs"}


class MessageRequest(mongoengine.Document):
    m_id = mongoengine.SequenceField(required=True)
    urgency = mongoengine.StringField(required=True)

    caller_name = mongoengine.StringField(required=True)
    caller_number = mongoengine.StringField(required=True)

    called_name = mongoengine.StringField(required=True)
    called_num = mongoengine.StringField(required=True)

    message = mongoengine.StringField(required=False)

    meta = {"db_alias": "core", "collection": "messageRequests"}
