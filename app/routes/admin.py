from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.models import URL
from app import schema

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/url", response_model=schema.URL, status_code=status.HTTP_200_OK)
async def admin(key: schema.Key) -> schema.URL:
    """
    Retrieve the URL associated with the provided admin key.

    :param key: The admin key used to look up the URL.
    :return: The URL object if found.
    :raises HTTPException: If the URL does not exist or the admin key is invalid.
    """
    exist_url = await URL.filter(admin_url=key.key).first()
    if exist_url is None:
        message = "This URL does not exist in the database or admin key is not valid."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return exist_url
