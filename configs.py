from dotenv import load_dotenv

import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

app_config = {
    "title": "ZipLink",
    "description": "ZipLink is a FastAPI-based URL shortener.",
    "contact": {
        "name": "AmirAli Irvani",
        "url": "https://github.com/irvaniamirali/zip-link",
        "email": "irvaniamirali.dev@gmail.com",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
}
