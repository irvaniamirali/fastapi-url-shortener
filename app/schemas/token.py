from pydantic import BaseModel


class Token(BaseModel):
    """Schema for returning access token and token type."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for data contained within a JWT token."""
    username: str | None = None
