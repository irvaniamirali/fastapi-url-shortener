from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url="sqlite://zip-link.sqlite3",
        modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()
