from fastapi import APIRouter, HTTPException
from core.database import db
from core.config import OWNER_ID
import datetime

router = APIRouter()


# =====================================
# Simple Owner Protection
# (Replace with token auth in production)
# =====================================
def check_owner(user_id: int):
    if user_id != OWNER_ID:
        raise HTTPException(status_code=403, detail="Unauthorized")


# =====================================
# Admin Management
# =====================================
@router.get("/admins")
async def list_admins():
    admins = []
    async for admin in db.admins.find():
        admins.append(admin["user_id"])
    return {"admins": admins}


@router.post("/admins/add/{user_id}")
async def add_admin(user_id: int):
    await db.admins.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )
    return {"status": "admin added"}


@router.delete("/admins/remove/{user_id}")
async def remove_admin(user_id: int):
    await db.admins.delete_one({"user_id": user_id})
    return {"status": "admin removed"}


# =====================================
# ForceSub Management
# =====================================
@router.get("/forcesub")
async def list_forcesub():
    channels = []
    async for ch in db.force_sub.find():
        channels.append(ch["channel_id"])
    return {"channels": channels}


@router.post("/forcesub/add/{channel_id}")
async def add_forcesub(channel_id: int):
    await db.force_sub.update_one(
        {"channel_id": channel_id},
        {"$set": {"channel_id": channel_id}},
        upsert=True
    )
    return {"status": "forcesub added"}


@router.delete("/forcesub/remove/{channel_id}")
async def remove_forcesub(channel_id: int):
    await db.force_sub.delete_one({"channel_id": channel_id})
    return {"status": "forcesub removed"}


# =====================================
# Premium Management
# =====================================
@router.get("/premium")
async def list_premium():
    users = []
    async for user in db.premium.find():
        users.append({
            "user_id": user["user_id"],
            "expiry": user["expiry"]
        })
    return {"premium_users": users}


@router.post("/premium/add/{user_id}/{days}")
async def add_premium(user_id: int, days: int):

    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=days)

    await db.premium.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "expiry": expiry}},
        upsert=True
    )

    return {"status": "premium added", "expiry": expiry}


@router.delete("/premium/remove/{user_id}")
async def remove_premium(user_id: int):
    await db.premium.delete_one({"user_id": user_id})
    return {"status": "premium removed"}
