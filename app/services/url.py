from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import selectinload
from typing import List
import logging

from app.models.url import Url
from app.models.click_log import ClickLog
from app.schemas.url import UrlCreate, UrlUpdate
from app.utils import generate_short_code

logger = logging.getLogger(__name__)


async def create_short_url(
        db: AsyncSession,
        user_id: int | None,
        url_create: UrlCreate,
) -> Url:
    """
    Creates a new shortened URL in the database.
    Supports custom short codes, expiration dates, max clicks limit, and one-time use.
    """
    short_code = url_create.custom_short_code
    if short_code:
        # Check if custom short code is already in use
        existing_url = await db.execute(select(Url).where(Url.short_code == short_code))
        if existing_url.scalar_one_or_none():
            logger.warning(f"Attempt to create URL with existing custom short code: {short_code}")
            raise ValueError(f"Custom short code '{short_code}' is already in use.")
        logger.info(f"Using custom short code: {short_code}")
    else:
        short_code = await _generate_unique_short_code(db)
        logger.info(f"Generated random short code: {short_code}")

    new_url = Url(
        original_url=str(url_create.original_url),
        short_code=short_code,
        user_id=user_id,
        expired_at=url_create.expired_at,
        max_clicks=url_create.max_clicks,
        one_time_use=url_create.one_time_use,
    )

    try:
        db.add(new_url)
        await db.commit()
        await db.refresh(new_url)
        logger.info(f"URL created successfully: ID {new_url.id}, Short Code: {new_url.short_code}")
        return new_url
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error during URL creation for {url_create.original_url}: {e}")
        raise ValueError("Failed to create URL, possibly due to a unique constraint violation.") from e
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error during URL creation for {url_create.original_url}: {e}")
        raise SQLAlchemyError(f"A database error occurred during URL creation.") from e
    except Exception as e:
        await db.rollback()
        logger.critical(f"Unexpected error during URL creation for {url_create.original_url}: {e}", exc_info=True)
        raise Exception(f"An unexpected error occurred during URL creation.") from e


async def _generate_unique_short_code(db: AsyncSession) -> str:
    """
    Generates a unique random short code that does not yet exist in the database.
    """
    while True:
        short_code = generate_short_code()
        result = await db.execute(select(Url).where(Url.short_code == short_code))
        if result.scalar_one_or_none() is None:
            return short_code


async def get_user_urls(db: AsyncSession, user_id: int) -> List[Url]:
    """
    Retrieves all shortened URLs associated with a specific user ID.
    """
    logger.info(f"Fetching URLs for user ID: {user_id}")
    result = await db.execute(select(Url).where(Url.user_id == user_id))
    return result.scalars().all()


async def get_url_by_id(db: AsyncSession, url_id: int, user_id: int) -> Url | None:
    """
    Retrieves a specific URL by its ID, ensuring it belongs to the specified user.
    """
    logger.debug(f"Fetching URL ID {url_id} for user ID {user_id}")
    result = await db.execute(
        select(Url).where(Url.id == url_id, Url.user_id == user_id)
    )
    url = result.scalar_one_or_none()
    if not url:
        logger.warning(f"URL ID {url_id} not found or not owned by user {user_id}")
    return url


async def update_url(db: AsyncSession, url_id: int, user_id: int, url_update: UrlUpdate) -> Url | None:
    """
    Updates an existing URL's details, ensuring it belongs to the specified user.
    """
    logger.info(f"Attempting to update URL ID {url_id} for user ID {user_id}")
    result = await db.execute(
        select(Url).where(Url.id == url_id, Url.user_id == user_id)
    )
    url = result.scalar_one_or_none()
    if not url:
        logger.warning(f"URL update failed: ID {url_id} not found or not allowed for update by user {user_id}.")
        return None

    update_data = url_update.model_dump(exclude_unset=True, mode="json")
    for key, value in update_data.items():
        setattr(url, key, value)

    if url.one_time_use:
        logger.info(f"URL ID {url.id} set to one-time use.")
        url.max_clicks = 1

    try:
        await db.commit()
        await db.refresh(url)
        logger.info(f"URL ID {url.id} updated successfully.")
        return url
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error updating URL ID {url_id} for user {user_id}: {e}")
        raise SQLAlchemyError(f"Error updating URL: {e}") from e
    except Exception as e:
        await db.rollback()
        logger.critical(f"Unexpected error during URL update for ID {url_id}: {e}", exc_info=True)
        raise Exception(f"An unexpected error occurred during URL update: {e}") from e


async def delete_url_by_id(db: AsyncSession, url_id: int, user_id: int) -> bool:
    """
    Deletes a specific URL from the database, ensuring it belongs to the specified user.
    """
    logger.info(f"Attempting to delete URL ID {url_id} for user ID {user_id}")
    result = await db.execute(
        select(Url).where(Url.id == url_id, Url.user_id == user_id)
    )
    url = result.scalar_one_or_none()
    if not url:
        logger.warning(f"URL ID {url_id} not found or not allowed for deletion by user {user_id}.")
        return False

    try:
        await db.delete(url)
        await db.commit()
        logger.info(f"URL ID {url.id} deleted successfully.")
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error deleting URL ID {url_id} for user {user_id}: {e}")
        raise SQLAlchemyError(f"Error deleting URL: {e}") from e
    except Exception as e:
        await db.rollback()
        logger.critical(f"Unexpected error during URL deletion for ID {url_id}: {e}", exc_info=True)
        raise Exception(f"An unexpected error occurred during URL deletion: {e}") from e


async def log_click(
        db: AsyncSession,
        url_id: int,
        referrer: str | None,
        user_agent: str | None,
        ip_address: str | None
) -> ClickLog:
    """
    Logs a click event for a given URL.
    """
    new_click_log = ClickLog(
        url_id=url_id,
        referrer=referrer,
        user_agent=user_agent,
        ip_address=ip_address,
    )
    try:
        db.add(new_click_log)
        await db.commit()
        await db.refresh(new_click_log)
        logger.debug(f"Click logged for URL ID {url_id}. Referrer: {referrer}")
        return new_click_log
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error logging click for URL ID {url_id}: {e}")
        raise SQLAlchemyError(f"Failed to log click: {e}") from e
    except Exception as e:
        await db.rollback()
        logger.critical(f"Unexpected error logging click for URL ID {url_id}: {e}", exc_info=True)
        raise Exception(f"An unexpected error occurred during click logging: {e}") from e


async def get_url_analytics(db: AsyncSession, url_id: int, user_id: int) -> Url | None:
    """
    Retrieves a URL along with its full click logs for analytics.
    Ensures the URL belongs to the specified user.
    """
    logger.info(f"Fetching analytics for URL ID {url_id} by user {user_id}")
    # Load URL and its related click logs
    result = await db.execute(
        select(Url).where(Url.id == url_id, Url.user_id == user_id)
        .options(selectinload(Url.click_logs))
    )
    url = result.scalar_one_or_none()
    if not url:
        logger.warning(f"Analytics requested for URL ID {url_id} not found or not owned by user {user_id}")
        return None

    total_clicks = url.clicks
    logger.info(f"Analytics fetched for URL ID {url_id}. Total clicks: {total_clicks}")
    return url
