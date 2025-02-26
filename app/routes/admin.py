from fastapi import APIRouter, Body, Depends, BackgroundTasks, status
from fastapi.exceptions import HTTPException
from datetime import datetime
from typing import Optional

from app.utils import run_task, generate_random_string
from app.models import Admin, URL
from app import schema

router = APIRouter(prefix="/admin", tags=["Admin"])


async def delete_url(key):
    record = await URL.filter(key=key).first()
    await record.delete()


async def get_current_admin(admin_key: str = Body(max_length=12)):
    admin = await Admin.get_or_none(admin_key=admin_key)
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin key")
    return admin


@router.post("/", response_model=schema.AdminKey, status_code=status.HTTP_200_OK)
async def create_admin_key():
    """
    Generate a new admin key.

    :return: The newly created admin key.
    """
    return await Admin.create(admin_key=generate_random_string(12))


@router.post("/url", response_model=schema.URLBase, status_code=status.HTTP_200_OK)
async def create(
        background_tasks: BackgroundTasks,
        url: schema.AnyUrl,
        expire: Optional[datetime] = Body(default=None),
        admin: Admin = Depends(get_current_admin)
):
    """
    Create a new URL if it does not already exist.

    :param expire:
    :param background_tasks:
    :param admin:
    :param url: The URL data to be created.
    :return: The created URL object.
    """
    key = generate_random_string()

    if expire is not None:
        background_tasks.add_task(run_task, run_time=url, coro=delete_url(key))

    return await URL.create(url=url, key=key, expire=expire, admin=admin)


@router.get("/url", response_model=schema.URLBase, status_code=status.HTTP_200_OK)
async def fetch_url_information(key: str = Body(), admin: Admin = Depends(get_current_admin)):
    """
    Retrieve the URL associated with the admin key.

    :param key: The admin key used to look up the URL.
    :param admin: The current admin making the request.
    :return: The URL object if found.
    :raises HTTPException: If the URL does not exist or the admin key is invalid.
    """
    exist_url = await URL.filter(admin=admin, key=key).first()

    if exist_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This URL does not exist in the database or admin key is not valid."
        )

    return exist_url


@router.put("/url", response_model=schema.URLBase, status_code=status.HTTP_200_OK)
async def update(
        background_tasks: BackgroundTasks,
        url: schema.constr(max_length=255) = Body(),
        key: schema.constr(min_length=6, max_length=6, pattern=r'^[a-zA-Z0-9]+$') = Body(),
        expire: Optional[datetime] = Body(default=None),
        admin: Admin = Depends(get_current_admin)
):
    """
    Update an existing URL entry for the specified admin.

    Parameters:
    - background_tasks: Background tasks to be run after the response.
    - url: The new URL to be updated.
    - key: The unique key identifying the URL entry.
    - expire: Optional expiration time for the URL.
    - admin: The admin object for authorization.

    Returns:
    - The updated URL entry.
    """
    exist_url = await URL.filter(key=key, admin=admin).first()

    if exist_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The URL key or admin key is invalid."
        )

    if expire is not None:
        background_tasks.add_task(run_task, run_time=expire, coro=delete_url(key))

    return await exist_url.update_from_dict({"url": url, "expire": expire})
