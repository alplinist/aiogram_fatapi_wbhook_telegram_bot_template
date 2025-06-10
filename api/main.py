from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.database import init_db, close_db
from core.redis import init_redis, close_redis
from core.config import WEBHOOK_URL
from bot.bot import bot
from api.routes.webhook import router as webhook_router
from api.routes.miniapp import router as miniapp_router
from api.routes.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    await bot.set_webhook(url=WEBHOOK_URL)
    yield
    await bot.delete_webhook()
    await close_redis()
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(webhook_router)
app.include_router(miniapp_router)
app.include_router(admin_router)
