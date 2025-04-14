from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from tortoise.contrib.fastapi import register_tortoise

from app.handlers import custom_http_exception_handler
from app.middleware import add_middlewares
from configs import app_config, settings
from app.routers import router

app = FastAPI(**app_config)

app.add_exception_handler(HTTPException, custom_http_exception_handler)  # type: ignore

# Add all middlewares here
add_middlewares(app)

register_tortoise(
    app,
    db_url=settings.database_host,
    modules={
        "models": [
            "app.models.users",
            "app.models.urls",
            "app.models.rate_limiter"
        ]
    },
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "It seems good; Visit the /docs page"}


app.include_router(router)
