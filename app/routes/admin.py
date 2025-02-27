from fastapi import APIRouter, Body, Depends, BackgroundTasks, status
from fastapi.exceptions import HTTPException
from datetime import datetime
from typing import Optional, List, Union

from app.utils import run_task, generate_random_string
from app.models import Admin, URL
from app import schema

router = APIRouter(prefix="/admin", tags=["Admin"])


async def delete_url(key):
    record = await URL.filter(key=key).first()
    await record.delete()


async def get_current_admin(admin_key: Union[str, dict] = Body()):
    if isinstance(admin_key, str):
        admin_key = admin_key
    elif isinstance(admin_key, dict):
        admin_key = admin_key.get("admin_key")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admin input format")

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
        url: schema.AnyUrl = Body(...),
        expire: Optional[datetime] = Body(default=None),
        is_active: Optional[bool] = Body(default=True),
        admin: Admin = Depends(get_current_admin)
):
    """
    Create a new URL entry if it does not already exist.

    Parameters:
    - url: The URL to be created.
    - expire: Optional expiration datetime for the URL.
    - is_active: Flag to indicate if the URL is active (default is True).
    - background_tasks: Allows adding background tasks.
    - admin: The admin user making the request.

    Returns:
    - The created URL object.
    """
    key = generate_random_string()

    if expire is not None:
        background_tasks.add_task(run_task, run_time=expire, coro=delete_url(key))

    return await URL.create(url=url, key=key, expire=expire, is_active=is_active, admin=admin)


@router.get("/url", response_model=schema.URLBase, status_code=status.HTTP_200_OK)
async def fetch_url_information(
        key: schema.constr(min_length=6, max_length=6, pattern=r'^[a-zA-Z0-9]+$') = Body(...),
        admin: Admin = Depends(get_current_admin)
):
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
            detail="This URL does not exist in the database or admin key is not valid"
        )

    return exist_url


@router.put("/url", response_model=schema.URLBase, status_code=status.HTTP_200_OK)
async def update(
        background_tasks: BackgroundTasks,
        key: schema.constr(min_length=6, max_length=6, pattern=r'^[a-zA-Z0-9]+$') = Body(...),
        url: Optional[schema.AnyUrl] = Body(default=None),
        expire: Optional[datetime] = Body(default=None),
        is_active: Optional[bool] = Body(default=None),
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
            detail="The URL key or admin key is invalid"
        )

    if url is None:
        url = exist_url.url

    if is_active is None:
        is_active = exist_url.is_active

    if expire is not None:
        background_tasks.add_task(run_task, run_time=expire, coro=delete_url(key))

    args = {"url": url, "expire": expire, "is_active": is_active}
    updated_url = await exist_url.update_from_dict(args)
    await updated_url.save()
    return updated_url


@router.delete("/url", status_code=status.HTTP_200_OK)
async def delete(admin: Admin = Depends(get_current_admin)):
    """
    Delete the URL associated with the current admin.

    :param admin: The currently authenticated admin.
    :return: A confirmation message indicating that the URL has been deleted.
    :raises HTTPException: If the admin does not have an associated URL.
    """
    exist_url = await URL.filter(admin=admin).first()

    if exist_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The Admin Key is invalid."
        )

    await exist_url.delete()
    return {"message": "The URL has been deleted."}


@router.get("/urls", response_model=List[schema.URLBase], status_code=status.HTTP_200_OK)
async def list_urls(admin: Admin = Depends(get_current_admin)):
    """
    Retrieve all URLs associated with the current admin.

    :param admin: The current admin making the request.
    :return: A list of URL objects.
    """
    return await URL.filter(admin=admin).all()
