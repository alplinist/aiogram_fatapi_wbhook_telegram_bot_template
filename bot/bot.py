from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from core.config import BOT_TOKEN
from bot.handlers.user_flow import user_router

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

dp = Dispatcher()

dp.include_router(user_router)
