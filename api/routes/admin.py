from fastapi import APIRouter, UploadFile, File
from io import BytesIO
import openpyxl

from core import models
from bot.bot import bot

router = APIRouter(prefix="/admin")


@router.post("/upload")
async def upload_orders(file: UploadFile = File(...)):
    data = await file.read()
    workbook = openpyxl.load_workbook(BytesIO(data))
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        tracking_number = str(row[0]).strip()
        telegram_id = int(row[1]) if row[1] else None
        weight = float(row[2]) if row[2] else None

        if not telegram_id:
            continue

        user = await models.User.get_or_none(telegram_id=telegram_id)
        if user is None:
            continue

        order, _ = await models.Order.get_or_create(
            tracking_number=tracking_number,
            defaults={"user": user, "weight": weight},
        )
        if weight is not None:
            order.weight = weight
            await order.save()
        await bot.send_message(
            user.telegram_id,
            f"Order {tracking_number} added/updated",
        )

    return {"status": "processed"}
