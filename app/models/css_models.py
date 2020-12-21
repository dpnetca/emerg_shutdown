from typing import Optional, List
import uuid
from pydantic import BaseModel


class css(BaseModel):
    name: str
    uuid: uuid.UUID


class css_member(BaseModel):
    name: str
    pt_uuid: uuid.UUID
    member_uuid: uuid.UUID


class css_detail(css):
    description: Optional[str]
    members: Optional[List[css_member]]
