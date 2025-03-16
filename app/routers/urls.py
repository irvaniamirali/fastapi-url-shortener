from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks, Body, status
from datetime import datetime
from typing import List, Annotated

from app import utils
from app.models import User, URL
from app.schema import URLCreate, URLBase, URLUpdate, Key
from app.dependencies import get_current_user

router = APIRouter(prefix="/urls", tags=["URLs"])

def is_future_date(dt):
    return datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S") < datetime.now()

def future_date_exception():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="The expiration date must be in the future. Please enter a valid date"
    )

def url_record_missing_exception():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="This URL does not exist in the database or the key you provided is not valid."
    )

async def delete_url(key, user=None):
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

    :param background_tasks: Allows adding background tasks.
    :param url: URLCreate schema containing URL details.
    :param user: The current authenticated user.
    :return: The created URLBase object.
    """
    key = utils.generate_random_string()

    if url.expire_date:
        if is_future_date(url.expire_date):
            raise future_date_exception

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

    :param key: Key schema containing the URL key.
    :param user: The current authenticated user.
    :return: The URLBase object if found.
    :raises HTTPException: If the URL is not found or key is invalid.
    """
    exist_url = await URL.filter(user=user, key=key.key).first()

    if not exist_url:
        raise url_record_missing_exception()

    return exist_url


@router.put("/", response_model=URLBase, status_code=status.HTTP_200_OK)
async def update(
        background_tasks: BackgroundTasks,
        user: Annotated[User, Depends(get_current_user)],
        url: URLUpdate = Body(...)
):
    """
    Update an existing URL entry for the authenticated user.

    :param background_tasks: Allows adding background tasks.
    :param url: URLUpdate schema containing updated URL details.
    :param user: The current authenticated user.
    :return: The updated URLBase object.
    :raises HTTPException: If the URL or key is invalid.
    """
    exist_url = await URL.filter(key=url.key, user=user).first()

    if not exist_url:
        raise url_record_missing_exception()

    if url.expire_date:
        if is_future_date(url.expire_date):
            future_date_exception()

        background_tasks.add_task(utils.run_task, run_time=url.expire_date, coro=delete_url(url.key))

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

    :param key: Key schema containing the URL key.
    :param user: The current authenticated user.
    :return: Confirmation message upon successful deletion.
    :raises HTTPException: If the URL key or user key is invalid.
    """
    exist_url = await delete_url(key, user)

    if not exist_url:
        raise url_record_missing_exception()

    return {"message": "The URL has been deleted"}


@router.get("/all", response_model=List[URLBase], status_code=status.HTTP_200_OK)
async def list_urls(user: Annotated[User, Depends(get_current_user)]):
    """
    Retrieve all URLs associated with the authenticated user.

    :param user: The current authenticated user.
    :return: A list of URLBase objects.
    """
    return await URL.filter(user=user).all()
