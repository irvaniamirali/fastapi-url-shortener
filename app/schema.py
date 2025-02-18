from pydantic import BaseModel, AnyUrl


class URLCreate(BaseModel):
    target_url: AnyUrl


class URL(URLCreate):
    secret_key: str
    clicks: int
