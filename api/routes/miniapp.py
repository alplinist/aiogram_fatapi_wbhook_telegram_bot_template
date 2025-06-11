from fastapi import APIRouter, Response
from core import models
from core.database import init_db
from api.schemas import UserCreate, AddressCreate, OrderCreate, OrderUpdate
from bot.bot import bot

router = APIRouter(prefix="/api")

@router.post("/register")
async def register_user(data: UserCreate):
    user, created = await models.User.get_or_create(
        telegram_id=data.telegram_id, defaults=data.model_dump()
    )
    if not created:
        await user.update_from_dict(data.model_dump()).save()
    return {"id": user.id, "telegram_id": user.telegram_id}

@router.post("/orders")
async def create_order(data: OrderCreate):
    user = await models.User.get(id=data.user_id)
    order = await models.Order.create(
        user=user,
        tracking_number=data.tracking_number,
        status=data.status,
        weight=data.weight,
    )
    return {"order_id": order.id}

@router.post("/orders/{tracking_number}")
async def update_order(tracking_number: str, data: OrderUpdate):
    order = await models.Order.get_or_none(tracking_number=tracking_number)
    if order is None:
        return Response(status_code=404)

    changes: list[str] = []
    if data.status is not None and data.status != order.status:
        order.status = data.status
        changes.append(f"Status changed to {data.status}")
    if data.weight is not None and data.weight != order.weight:
        order.weight = data.weight
        changes.append(f"Weight set to {data.weight}")
    await order.save()

    if changes:
        await order.fetch_related("user")
        await bot.send_message(order.user.telegram_id, "\n".join(changes))

    return {"status": "updated"}

@router.get("/orders/{user_id}")
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

@router.get("/addresses/{user_id}")
async def list_addresses(user_id: int):
    user = await models.User.get(id=user_id)
    await user.fetch_related("addresses")
    addresses = [
        {"id": a.id, "address": a.address, "is_default": a.is_default}
        for a in user.addresses
    ]
    return {"addresses": addresses}

@router.post("/addresses")
async def add_address(data: AddressCreate):
    user = await models.User.get(id=data.user_id)
    addr = await models.Address.create(
        user=user, address=data.address, is_default=data.is_default
    )
    return {"address_id": addr.id}
