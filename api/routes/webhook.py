from fastapi import APIRouter, Request, Response
from aiogram.types import Update

from bot.bot import bot, dp
from core.config import WEBHOOK_PATH

router = APIRouter()

@router.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot=bot, update=update)
    return Response(status_code=200)
