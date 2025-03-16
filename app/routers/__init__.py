from fastapi import APIRouter

from .urls import router as urls_router
from .users import router as users_router
from .redirect import router as redirect_router

router = APIRouter()

router.include_router(users_router, prefix="/api")
router.include_router(urls_router, prefix="/api")
router.include_router(redirect_router)
