from fastapi import Depends, HTTPException
from core.models import User

async def get_user(user_id: int) -> User:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
