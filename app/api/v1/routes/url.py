from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse, Response
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.api.v1.deps import get_db, get_current_user
from app.schemas.url import UrlCreate, UrlUpdate, UrlOut, UrlAnalyticsOut, ClickLogOut
from app.models.user import User
from app.core.config import settings
from app.services.url import (
    create_short_url,
    get_user_urls,
    get_url_by_id,
    update_url,
    delete_url_by_id,
    get_url_analytics
)
from app.utils import generate_qr_code_base64

router = APIRouter(tags=["URLs"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=UrlOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new short URL",
    dependencies=[
        Depends(
            RateLimiter(
                times=settings.RATE_LIMIT_CREATE_URL_TIMES,
                seconds=settings.RATE_LIMIT_CREATE_URL_SECONDS
            )
        )
    ]
)
async def create_url(
        url_create: UrlCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Create a new shortened URL for the authenticated user.
    Supports custom short codes, expiration dates, max clicks limit, and one-time use.
    """
    logger.info(f"User {current_user.id} attempting to create URL: {url_create.original_url}")
    try:
        return await create_short_url(db, current_user.id, url_create)
    except ValueError as e:
        logger.warning(f"URL creation failed due to validation error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating URL for user {current_user.id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create URL.")


@router.get("/", response_model=List[UrlOut], summary="List all short URLs for the current user")
async def list_user_urls(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Retrieve a list of all shortened URLs owned by the current authenticated user.
    """
    logger.info(f"Fetching all URLs for user ID: {current_user.id}")
    return await get_user_urls(db, current_user.id)


@router.get("/{url_id}", response_model=UrlOut, summary="Get a short URL by its ID")
async def get_url(
        url_id: int = Path(..., description="The ID of the short URL to retrieve."),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Retrieve details of a specific short URL by its ID, ensuring it belongs to the current user.
    """
    url = await get_url_by_id(db, url_id, current_user.id)
    if not url:
        logger.warning(f"Request for URL ID {url_id} by user {current_user.id}: URL not found or not owned.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found or not owned by user.")
    logger.info(f"URL ID {url_id} retrieved successfully for user {current_user.id}.")
    return url


@router.put("/{url_id}", response_model=UrlOut, summary="Update an existing short URL")
async def update_url_endpoint(
        url_update: UrlUpdate,
        url_id: int = Path(..., description="The ID of the short URL to update."),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Update details of an existing short URL (e.g., original URL, expiration date, max clicks, one-time use).
    Only the owner of the URL can update it.
    """
    logger.info(f"User {current_user.id} attempting to update URL ID: {url_id}")
    updated_url = await update_url(db, url_id, current_user.id, url_update)
    if not updated_url:
        logger.warning(f"URL update failed: ID {url_id} not found or not allowed for user {current_user.id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found or not allowed.")
    logger.info(f"URL ID {url_id} updated successfully by user {current_user.id}.")
    return updated_url


@router.delete("/{url_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a short URL")
async def delete_url(
        url_id: int = Path(..., description="The ID of the short URL to delete."),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Delete a specific short URL. Only the owner of the URL can delete it.
    """
    logger.info(f"User {current_user.id} attempting to delete URL ID: {url_id}")
    success = await delete_url_by_id(db, url_id, current_user.id)
    if not success:
        logger.warning(f"URL deletion failed: ID {url_id} not found or not allowed for user {current_user.id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found or not allowed.")
    logger.info(f"URL ID {url_id} deleted successfully by user {current_user.id}.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{url_id}/qr", summary="Get QR Code for a short URL", response_class=JSONResponse)
async def get_qr_code(
        url_id: int = Path(..., description="The ID of the short URL to get QR code for."),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Generates and returns a Base64 encoded QR Code image for the specified short URL.
    """
    logger.info(f"User {current_user.id} requesting QR code for URL ID: {url_id}")
    url = await get_url_by_id(db, url_id, current_user.id)
    if not url:
        logger.warning(
            f"QR code request failed: URL ID {url_id} not found or not owned by user {current_user.id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found or not owned by user.")

    short_url = f"{settings.BASE_DOMAIN}/{url.short_code}"
    qr_code_base64 = generate_qr_code_base64(short_url)

    logger.info(f"QR code generated for URL ID {url_id}.")
    return JSONResponse(content={"qr_code_png_base64": qr_code_base64, "short_url": short_url})


@router.get(
    "/{url_id}/analytics",
    response_model=UrlAnalyticsOut,
    summary="Get analytics for a short URL"
)
async def get_url_analytics_endpoint(
        url_id: int = Path(..., description="The ID of the short URL to get analytics for."),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Retrieves detailed click analytics for a specific short URL, ensuring it belongs to the current user.
    """
    logger.info(f"User {current_user.id} requesting analytics for URL ID: {url_id}")
    url_with_logs = await get_url_analytics(db, url_id, current_user.id)

    if not url_with_logs:
        logger.warning(f"Analytics request failed: URL ID {url_id} not found or not owned by user {current_user.id}.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found or not owned by user.")

    return UrlAnalyticsOut(
        id=url_with_logs.id,
        original_url=str(url_with_logs.original_url),
        short_code=url_with_logs.short_code,
        clicks=url_with_logs.clicks,
        created_at=url_with_logs.created_at,
        expired_at=url_with_logs.expired_at,
        max_clicks=url_with_logs.max_clicks,
        one_time_use=url_with_logs.one_time_use,
        total_clicks=url_with_logs.clicks,
        click_logs=[ClickLogOut.model_validate(log) for log in url_with_logs.click_logs]
    )
