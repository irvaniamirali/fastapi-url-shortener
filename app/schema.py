from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    url: AnyUrl
    expire: Optional[datetime] = None


class URL(URLCreate):
    key: str
    clicks: int
    admin_url: str


class Key(BaseModel):
    key: str
