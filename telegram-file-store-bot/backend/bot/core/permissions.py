from core.database import db
from core.config import OWNER_ID


async def is_admin(user_id: int) -> bool:

    if user_id == OWNER_ID:
        return True

    admin = await db.admins.find_one({"user_id": user_id})
    return bool(admin)
