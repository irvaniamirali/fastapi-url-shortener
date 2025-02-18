from fastapi import APIRouter, Path, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException

from app.models import URL
from app import schema

router = APIRouter()

@router.post("/url/create", status_code=status.HTTP_200_OK)
async def create_url(url: schema.URLCreate) -> schema.URL:
    """
    Create a new URL if it does not already exist.

    :param url: The URL data to be created.
    :return: The created URL object.
    :raises HTTPException: If the URL already exists (409 Conflict).
    """
    for exist_url in await URL.all():
        if exist_url.target_url == str(url.target_url):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"This URL({url.target_url}) is already exist."
            )

    return await URL.create(target_url=url.target_url)


@router.get("/url", status_code=status.HTTP_200_OK)
async def get_url_information(secret_key: str) -> schema.URL:
    """
    Get detailed information about the URL associated with the given secret key.

    :param secret_key: The secret key associated with the URL.
    :return: Returns the information of the URL if it exists; raises a 404 error if not found.
    """
    exist_url = await URL.filter(secret_key=secret_key).first()
    if exist_url is None:
        message = "This URL does not exist in the database; please create it first."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return exist_url


@router.get("/{key}", status_code=status.HTTP_200_OK)
async def redirect(key: str = Path(max_length=8)) -> RedirectResponse:
    """
    Redirect the target URL associated with the provided secret key.

    :param key: The secret key associated with the URL.
    :return: A redirect response to the target URL if it exists; raises a 404 error if not found.
    """
    exist_url = await URL.filter(secret_key=key).first()
    if exist_url is None:
        message = "This URL does not exist in the database; please create it first."
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    exist_url.clicks += 1
    await exist_url.save()

    return RedirectResponse(exist_url.target_url)
