import random
import string
import asyncio
import datetime

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
