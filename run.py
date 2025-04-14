import uvicorn

from app.main import app
from configs import settings


if __name__ == '__main__':
    uvicorn.run(app, host=settings.uvicorn_host, port=settings.uvicorn_port)
