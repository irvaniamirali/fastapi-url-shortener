from typing import Optional
from passlib.context import CryptContext
from jose import jwt

import asyncio
import random
import string
import datetime

from app.configs import ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_random_digit_number():
    first_digit = random.randint(1, 9)
    remaining_digits = random.randint(10 ** 8, 10 ** 9 - 1)
    return int(f"{first_digit}{remaining_digits:08d}")

def generate_random_string(length=6):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

async def wait_until(dt):
    """
    Sleep until the specified datetime.
    """
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())

async def run_task(run_time, coro):
    await wait_until(run_time)
    return await coro

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
