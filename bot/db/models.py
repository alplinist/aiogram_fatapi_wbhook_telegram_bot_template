from enum import Enum
from tortoise import fields
from tortoise.models import Model


class OrderStatus(str, Enum):
    ordered = "ordered"
    received_in_china = "received_in_china"
    in_transit = "in_transit"
    arrived_in_uzbekistan = "arrived_in_uzbekistan"
    ready_for_pickup = "ready_for_pickup"


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    first_name = fields.CharField(max_length=255, null=True)
    last_name = fields.CharField(max_length=255, null=True)
    phone_number = fields.CharField(max_length=50, null=True)

    orders: fields.ReverseRelation["Order"]
    addresses: fields.ReverseRelation["Address"]


class Address(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="addresses")
    address = fields.TextField()
    is_default = fields.BooleanField(default=False)


class Order(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="orders")
    tracking_number = fields.CharField(max_length=255, unique=True)
    status = fields.CharEnumField(OrderStatus, default=OrderStatus.ordered)
    weight = fields.FloatField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
