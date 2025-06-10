from aiogram import Router, types
from aiogram.filters import Command
from bot.db.models import User

user_router = Router()


@user_router.message(Command("start"))
async def cmd_start(message: types.Message):
    user, _ = await User.get_or_create(
        telegram_id=message.from_user.id,
        defaults={
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        },
    )
    await message.answer(f"Hello, your internal ID is {user.id}")
