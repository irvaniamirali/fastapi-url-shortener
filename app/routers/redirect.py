from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import RedirectResponse
from app.models import URL
from app.errors import ErrorCode

router = APIRouter(tags=["Redirect URL"])


@router.get("/{key}", response_class=RedirectResponse, status_code=status.HTTP_200_OK)
async def redirect(key: str = Path(max_length=6)):
    """
    Redirect the target URL associated with the provided key.
    """
    exist_url = await URL.filter(key=key).first()

    if exist_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.URL_NOT_FOUND
        )

    if not exist_url.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ErrorCode.URL_DEACTIVATED
        )

    exist_url.clicks += 1
    await exist_url.save()

    return RedirectResponse(exist_url.url)
