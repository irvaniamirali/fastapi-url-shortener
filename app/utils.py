from asyncio import sleep as aiosleep
from datetime import datetime

import random
import string

def generate_random_digit_number():
    first_digit = str(random.randint(1, 9))
    remaining_digits = random.choices(range(10), k=8)
    return int(first_digit + ''.join(map(str, remaining_digits)))

def generate_random_string(length=6):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

async def wait_until(dt):
    """
    Sleep until the specified datetime.
    """
    now = datetime.now()
    await aiosleep((dt - now).total_seconds())

async def run_task(run_time, coro):
    await wait_until(run_time)
    return await coro
