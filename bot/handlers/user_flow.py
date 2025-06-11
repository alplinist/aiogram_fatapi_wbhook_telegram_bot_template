from aiogram import Router, types
from aiogram.filters import Command
from core.models import User, Order

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


@user_router.message(Command("add"))
async def cmd_add(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.answer("Usage: /add <tracking_number>")

    tracking = parts[1].strip()

    user, _ = await User.get_or_create(
        telegram_id=message.from_user.id,
        defaults={
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        },
    )

    order, _ = await Order.get_or_create(user=user, tracking_number=tracking)
    await message.answer(f"Tracking number {order.tracking_number} saved")


@user_router.message(Command("orders"))
async def cmd_orders(message: types.Message):
    user = await User.get_or_none(telegram_id=message.from_user.id)
    if not user:
        await message.answer("You are not registered.")
        return
    await user.fetch_related("orders")
    if not user.orders:
        await message.answer("No orders yet.")
        return
    lines = [
        f"{o.tracking_number}: {o.status}" + (f", {o.weight}kg" if o.weight else "")
        for o in user.orders
    ]
    await message.answer("\n".join(lines))
