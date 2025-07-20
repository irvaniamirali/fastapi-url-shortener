from fastapi import APIRouter

from .routes.auth import router as auth
from .routes.redirect import router as redirect
from .routes.url import router as url

router = APIRouter()

router.include_router(auth, prefix="/api/v1/auth")
router.include_router(redirect)
router.include_router(url, prefix="/api/v1/url")
