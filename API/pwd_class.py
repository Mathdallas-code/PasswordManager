from pydantic import BaseModel
from typing import Optional


class pwd(BaseModel):
    user: str
    pwd: str
    website: Optional[str] = None
