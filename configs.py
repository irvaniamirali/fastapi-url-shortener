from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    uvicorn_host: str = "127.0.0.1"
    uvicorn_port: int = 8000

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    database_host: str
    test_database_host: str

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379

    max_tokens: int = 10
    refill_rate_per_second: int = 1

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore

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
