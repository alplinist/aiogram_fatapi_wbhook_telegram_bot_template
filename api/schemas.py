from pydantic import BaseModel
from core.models import OrderStatus

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
    status: OrderStatus = OrderStatus.ordered
    weight: float | None = None

class OrderUpdate(BaseModel):
    status: OrderStatus | None = None
    weight: float | None = None
