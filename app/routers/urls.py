from fastapi import Depends, APIRouter, BackgroundTasks, Body, Query, status
from fastapi.exceptions import HTTPException
from datetime import datetime
from typing import Annotated

from app import utils
from app.models import User, URL
from app.schema.response import PaginatedResponse
from app.schema.urls import URLCreate, URLBase, URLUpdate, Key
from app.errors import ErrorCode
from app.dependencies import get_current_user

router = APIRouter(prefix="/urls", tags=["URLs"])


def is_future_date(dt: datetime) -> bool:
    return datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S") < datetime.now()

def future_date_exception():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorCode.FUTURE_DATE
    )

def url_record_missing_exception():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorCode.INVALID_URL_KEY
    )

async def delete_url(key: str, user: User = None):
    record = await URL.filter(key=key, user=user).first()
    await record.delete() if record else None


@router.post("/", response_model=URLBase, status_code=status.HTTP_201_CREATED)
async def create_url_shortcut(
        background_tasks: BackgroundTasks,
        user: Annotated[User, Depends(get_current_user)],
        url: URLCreate = Body(...),
):
    """
    Create a new URL entry for the authenticated user.
    """
    key = utils.generate_random_string()

    if url.expire_date and is_future_date(url.expire_date):
        raise future_date_exception()

    if url.expire_date:
        background_tasks.add_task(utils.run_task, run_time=url.expire_date, coro=delete_url(key, user))

    params = {
        "url": url.url,
        "key": key,
        "expire_date": url.expire_date,
        "is_active": url.is_active,
        "user": user
    }
    return await URL.create(**params)


@router.get("/", response_model=URLBase, status_code=status.HTTP_200_OK)
async def get_url_details(user: Annotated[User, Depends(get_current_user)], key: Key = Body(...)):
    """
    Retrieve URL details using a key for the authenticated user.
    """
    exist_url = await URL.filter(user=user, key=key.key).first()

    if not exist_url:
        raise url_record_missing_exception()

    return exist_url


@router.put("/", response_model=URLBase, status_code=status.HTTP_200_OK)
async def update_url(
        background_tasks: BackgroundTasks,
        user: Annotated[User, Depends(get_current_user)],
        url: URLUpdate = Body(...)
):
    """
    Update an existing URL entry for the authenticated user.
    """
    exist_url = await URL.filter(key=url.key, user=user).first()

    if not exist_url:
        raise url_record_missing_exception()

    if url.expire_date and is_future_date(url.expire_date):
        raise future_date_exception()

    if url.expire_date:
        background_tasks.add_task(utils.run_task, run_time=url.expire_date, coro=delete_url(url.key, user))

    args = {
        "url": url.url or exist_url.url,
        "expire_date": url.expire_date or exist_url.expire_date,
        "is_active": url.is_active if url.is_active is not None else exist_url.is_active
    }

    await exist_url.update_from_dict(args)
    await exist_url.save()
    return exist_url


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_url_entry(user: Annotated[User, Depends(get_current_user)], key: Key = Body(...)):
    """
    Delete a URL entry for the authenticated user.
    """
    exist_url = await URL.get_or_none(key=key.key, user=user)

    if not exist_url:
        raise url_record_missing_exception()

    await exist_url.delete()

    return {"message": "The URL has been deleted successfully."}


@router.get("/all", response_model=PaginatedResponse[URLBase], status_code=status.HTTP_200_OK)
async def list_urls(
    user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0, le=100)
):
    """
    Retrieve all URLs associated with the authenticated user, with pagination support.
    """
    total = await URL.filter(user=user).count()
    urls = await URL.filter(user=user).offset(skip).limit(limit)

    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=urls
    )
