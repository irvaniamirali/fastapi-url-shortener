from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.configs import app_config, DATABASE_URL
from app.routes import router

app = FastAPI(**app_config)

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={
        "models": [
            "app.models.users",
            "app.models.urls"
        ]
    },
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "ZipLink greets you! Visit the /docs page"}


app.include_router(router)
