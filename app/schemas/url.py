from pydantic import BaseModel, HttpUrl, ConfigDict, Field
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

class UrlCreate(BaseModel):
    """Schema for creating a new URL."""
    original_url: HttpUrl
    custom_short_code: str | None = Field(
        None,
        min_length=4,
        max_length=12,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Optional custom short code for the URL. Must be unique."
    )
    expired_at: datetime | None = None
    max_clicks: int | None = Field(None, ge=1, description="Optional maximum number of clicks before the URL expires. Must be at least 1.")
    one_time_use: bool = Field(False, description="If true, the URL expires after one click. Overrides max_clicks if true.")


class UrlOut(BaseModel):
    """Schema for returning shortened URL details."""
    id: int
    original_url: HttpUrl
    short_code: str = Field(..., description="The unique short code for the URL.")
    clicks: int = 0
    created_at: datetime
    expired_at: datetime | None = None
    max_clicks: int | None = None
    one_time_use: bool = Field(False, description="If true, the URL expires after one click.")

    model_config = ConfigDict(from_attributes=True)


class UrlUpdate(BaseModel):
    """Schema for updating an existing URL's details."""
    original_url: HttpUrl | None = None
    expired_at: datetime = None
    max_clicks: int | None = Field(None, ge=1)
    one_time_use: bool | None = None

class ClickLogOut(BaseModel):
    """Schema for returning click log details."""
    id: int
    url_id: int
    clicked_at: datetime
    referrer: str | None = None
    user_agent: str | None = None
    ip_address: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UrlAnalyticsOut(UrlOut):
    """Schema for returning URL details with aggregated analytics."""
    total_clicks: int = Field(..., description="Total number of clicks for this URL.")
    click_logs: List[ClickLogOut] = Field([], description="Detailed logs for each click.")

    model_config = ConfigDict(from_attributes=True)
