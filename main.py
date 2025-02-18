from fastapi import FastAPI

from app.database import init
from app.routes import router

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init the database and generate schemas.
    await init()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "ZipLink greets you! Visit the /docs page"}


app.include_router(router)
