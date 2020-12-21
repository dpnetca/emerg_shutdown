from pydantic import BaseModel


class emerg_status(BaseModel):
    status: str


class css_status(BaseModel):
    name: str
    pstn_blocked: bool
