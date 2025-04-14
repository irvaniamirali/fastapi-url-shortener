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

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            AnyUrl: lambda value: str(value),
        }
    }


class URLUpdate(Key):
    url: AnyUrl = None
    expire_date: Optional[datetime] = None
    is_active: Optional[bool] = True
