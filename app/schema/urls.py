from pydantic import BaseModel, AnyUrl
from datetime import datetime
from typing import Optional
from app.schema.key import Key


class URLCreate(BaseModel):
    url: AnyUrl
    expire_date: Optional[datetime] = None
    is_active: Optional[bool] = True


class URLBase(URLCreate, Key):
    clicks: int

class URLUpdate(Key, URLCreate):
    pass
