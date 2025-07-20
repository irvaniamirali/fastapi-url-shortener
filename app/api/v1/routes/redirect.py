from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.deps import get_db
from app.models.url import Url
from app.services.url import log_click
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Redirect"])


@router.get(
    "/{code}",
    include_in_schema=False,
    summary="Redirect short code to original URL"
)
async def redirect_to_target_url(
        request: Request,
        code: str = Path(..., description="The short code to redirect."),
        db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """
    Redirects a short code to its original long URL.
    Increments the click count, logs click details, and handles expiration/max clicks/one-time use.
    """
    logger.info(f"Redirect request for short code: {code}")
    result = await db.execute(select(Url).where(Url.short_code == code))
    url = result.scalar_one_or_none()

    if not url:
        logger.warning(f"Redirect failed: Short URL '{code}' not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found.")

    if url.expired_at and url.expired_at < datetime.now(url.expired_at.tzinfo):
        logger.warning(f"Redirect failed for '{code}': URL expired at {url.expired_at}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL expired.")

    if url.max_clicks is not None and url.clicks >= url.max_clicks:
        logger.warning(
            f"Redirect failed for '{code}': Max clicks limit reached ({url.clicks}/{url.max_clicks}).")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL limit reached.")

    referrer = request.headers.get("referer")
    user_agent = request.headers.get("user-agent")
    ip_address = request.client.host

    try:
        await log_click(db, url.id, referrer, user_agent, ip_address)
    except Exception as e:
        logger.error(f"Failed to log click for URL ID {url.id}: {e}", exc_info=True)

    url.clicks += 1

    if url.one_time_use:
        url.expired_at = func.now()
        logger.info(f"One-time use URL '{code}' consumed and expired.")

    try:
        await db.commit()
        await db.refresh(url)
        logger.info(f"Redirecting '{code}' to '{url.original_url}'. Clicks: {url.clicks}.")
        return RedirectResponse(url=url.original_url)
    except Exception as e:
        await db.rollback()
        logger.critical(
            f"Unexpected error during redirect and URL update for '{code}': {e}",
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during redirect."
        )
