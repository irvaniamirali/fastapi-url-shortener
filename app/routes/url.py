from fastapi import APIRouter, BackgroundTasks, status

from app.utils import generate_random_string, run_task
from app import schema
from app.models import URL

router = APIRouter(tags=["URL"])

async def delete_url(key):
    record = await URL.filter(key=key).first()
    await record.delete()


@router.post("/url",  response_model=schema.URL, status_code=status.HTTP_200_OK)
async def create_url(url: schema.URLCreate, background_tasks: BackgroundTasks):
    """
    Create a new URL if it does not already exist.

    :param url: The URL data to be created.
    :return: The created URL object.
    """
    key, admin_url = generate_random_string()

    if url.expire is not None:
        background_tasks.add_task(run_task, run_time=url.expire, coro=delete_url(key))

    return await URL.create(url=url.url, key=key, admin_url=admin_url, expire=url.expire)
