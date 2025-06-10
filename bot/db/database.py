from tortoise import Tortoise


async def init_db(db_url: str = "sqlite://db.sqlite3"):
    await Tortoise.init(db_url=db_url, modules={"models": ["bot.db.models"]})
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
