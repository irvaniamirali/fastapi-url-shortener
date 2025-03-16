import asyncio
import random
import string
import datetime

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
