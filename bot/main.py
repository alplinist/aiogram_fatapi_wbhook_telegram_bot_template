import asyncio
from enum import Enum
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import Update
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from contextlib import asynccontextmanager

from bot.config import BOT_TOKEN, WEBHOOK_PATH, WEBHOOK_URL
from handlers.user_flow import user_router
from bot.db.database import init_db, close_db
from bot.db import models


class UserCreate(BaseModel):
    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None


class AddressCreate(BaseModel):
    user_id: int
    address: str
    is_default: bool = False


class OrderCreate(BaseModel):
    user_id: int
    tracking_number: str
    status: models.OrderStatus = models.OrderStatus.ordered
    weight: float | None = None


class OrderUpdate(BaseModel):
    status: models.OrderStatus | None = None
    weight: float | None = None



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
async def lifespan(app: FastAPI):
    await init_db()
    await bot.set_webhook(url=WEBHOOK_URL)
    print("🔗 Webhook set:", WEBHOOK_URL)
    print("WEBHOOK_PATH:", WEBHOOK_PATH)
    try:
        yield
    finally:
        await bot.delete_webhook()
        await close_db()
        print("❌ Webhook deleted")




# Create FastAPI app with webhook lifespan manager
app = FastAPI(lifespan=lifespan)


@app.post("/api/register")
async def register_user(data: UserCreate):
    user, created = await models.User.get_or_create(
        telegram_id=data.telegram_id, defaults=data.model_dump()
    )
    if not created:
        await user.update_from_dict(data.model_dump()).save()
    return {"id": user.id, "telegram_id": user.telegram_id}


@app.post("/api/orders")
async def create_order(data: OrderCreate):
    user = await models.User.get(id=data.user_id)
    order = await models.Order.create(
        user=user,
        tracking_number=data.tracking_number,
        status=data.status,
        weight=data.weight,
    )
    return {"order_id": order.id}


@app.post("/api/orders/{tracking_number}")
async def update_order(tracking_number: str, data: OrderUpdate):
    order = await models.Order.get_or_none(tracking_number=tracking_number)
    if order is None:
        return Response(status_code=404)
    if data.status is not None:
        order.status = data.status
    if data.weight is not None:
        order.weight = data.weight
    await order.save()
    return {"status": "updated"}


@app.get("/api/orders/{user_id}")
async def list_orders(user_id: int):
    user = await models.User.get(id=user_id)
    await user.fetch_related("orders")
    orders = [
        {
            "tracking_number": o.tracking_number,
            "status": o.status,
            "weight": o.weight,
        }
        for o in user.orders
    ]
    return {"orders": orders}


@app.get("/api/addresses/{user_id}")
async def list_addresses(user_id: int):
    user = await models.User.get(id=user_id)
    await user.fetch_related("addresses")
    addresses = [
        {"id": a.id, "address": a.address, "is_default": a.is_default}
        for a in user.addresses
    ]
    return {"addresses": addresses}


@app.post("/api/addresses")
async def add_address(data: AddressCreate):
    user = await models.User.get(id=data.user_id)
    addr = await models.Address.create(
        user=user, address=data.address, is_default=data.is_default
    )
    return {"address_id": addr.id}




# ✅ Manual webhook route that receives Telegram updates
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request:Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot=bot, update=update)
    return Response(status_code=200)
