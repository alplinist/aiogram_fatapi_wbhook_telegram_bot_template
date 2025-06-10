from tortoise import Tortoise
from .config import DATABASE_URL

async def init_db() -> None:
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["core.models"]})
    await Tortoise.generate_schemas()

async def close_db() -> None:
    await Tortoise.close_connections()
