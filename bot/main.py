import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from bot.config import BOT_TOKEN, WEBHOOK_PATH,WEBHOOK_URL
from handlers.user_flow import user_router
from bot.middlewares import LoggingMiddleware
from fastapi import FastAPI, Request,Response
from contextlib import asynccontextmanager
from aiogram.webhook.aiohttp_server import setup_application
from aiogram.types import Update



# 2. Init bot & dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# register user router 
dp.include_router(user_router)



# Register multimple routers (from user_flow.py, admin_panel.py, etc.)
# for router in routers:
#      dp.include_router(router)



# ✅ Lifespan: startup and shutdown logic
@asynccontextmanager
async def lifespan(app:FastAPI):
    await bot.set_webhook(url=WEBHOOK_URL)
    print("🔗 Webhook set:", WEBHOOK_URL)
    print("WEBHOOK_PATH:", WEBHOOK_PATH)
    yield
    await bot.delete_webhook()
    print("❌ Webhook deleted")




# Create FastAPI app with webhook lifespan manager
app = FastAPI(lifespan=lifespan)




# ✅ Manual webhook route that receives Telegram updates
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request:Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot=bot, update=update)
    return Response(status_code=200)
