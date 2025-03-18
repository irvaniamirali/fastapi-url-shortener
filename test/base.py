from tortoise import Tortoise, run_async

from app.configs import DATABASE_URL


async def init():
   await Tortoise.init(
       db_url=DATABASE_URL,
       modules={'models': ['app.models.users']}
   )
   await Tortoise.generate_schemas()
