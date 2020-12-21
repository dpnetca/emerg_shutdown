from typing import Optional, Callable
from pydantic import BaseModel


class Command(BaseModel):
    # name: str
    description: Optional[str]
    func: Callable
    has_args: bool = False
