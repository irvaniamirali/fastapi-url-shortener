import random
import string
import asyncio
import datetime

def generate_random_string():
    letters = string.ascii_letters + string.digits
    random_string = lambda length : ''.join(random.choice(letters) for i in range(length))
    return random_string(6), random_string(8)


async def wait_until(dt):
    """
    Sleep until the specified datetime.
    """
    now = datetime.datetime.now()
    await asyncio.sleep((dt - now).total_seconds())


async def run_task(run_time, coro):
    await wait_until(run_time)
    return await coro
