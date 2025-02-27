from pydantic import BaseModel, AnyUrl, constr
from datetime import datetime
from typing import Optional

class Key(BaseModel):
    key: constr(min_length=6, max_length=6, pattern=r'^[a-zA-Z0-9]+$')

class AdminKey(BaseModel):
    admin_key: constr(min_length=12, max_length=12, pattern=r'^[a-zA-Z0-9]+$')


class Create(BaseModel):
    url: AnyUrl
    expire: Optional[datetime] = None
    is_active: Optional[bool] = True


class URLBase(Create, Key):
    clicks: int
