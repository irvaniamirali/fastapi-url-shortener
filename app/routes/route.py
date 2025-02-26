from fastapi import APIRouter

from .admin import router as admin_router
from .url import router as url_router
from .redirect import router as redirect_router

router = APIRouter()

router.include_router(admin_router, prefix="/api")
router.include_router(url_router, prefix="/api")
router.include_router(redirect_router)
