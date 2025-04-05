from tortoise import Tortoise, run_async

from configs import DATABASE_URL

async def init():
   await Tortoise.init(
       db_url=DATABASE_URL,
       modules={
           'models': [
               'app.models.users',
               'app.models.urls'
           ]
       }
   )
   await Tortoise.generate_schemas()
