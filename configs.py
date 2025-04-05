from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

HOST = getenv("HOST", "127.0.0.1")
PORT = int(getenv("PORT", "8000"))

app_config = {
    "title": "FastAPI URL Shortener",
    "description": "FastAPI-based URL Shortener",
    "contact": {
        "name": "AmirAli Irvani",
        "url": "https://github.com/irvaniamirali/fastapi-url-shortener",
        "email": "irvaniamirali.dev@gmail.com",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
}
