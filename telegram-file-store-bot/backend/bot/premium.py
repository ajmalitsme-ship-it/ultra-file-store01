import datetime
from pyrogram import filters

from core.database import db
from core.permissions import is_admin


# =====================================
# Premium Check Function (Used Globally)
# =====================================

async def is_premium(user_id: int) -> bool:

    user = await db.premium.find_one({"user_id": user_id})

    if not user:
        return False

    if user["expiry"] < datetime.datetime.utcnow():
        # Auto remove expired premium
        await db.premium.delete_one({"user_id": user_id})
        return False

    return True


# =====================================
# Register Premium Commands
# =====================================

def register_premium(app):

    # -----------------------------
    # Add Premium
    # -----------------------------
    @app.on_message(filters.command("addpremium") & filters.private)
    async def add_premium(_, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) != 3:
            await message.reply("Usage: /addpremium user_id days")
            return

        try:
            user_id = int(message.command[1])
            days = int(message.command[2])
        except ValueError:
            await message.reply("Invalid input.")
            return

        expiry = datetime.datetime.utcnow() + datetime.timedelta(days=days)

        await db.premium.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id, "expiry": expiry}},
            upsert=True
        )

        await message.reply(f"Premium added until {expiry.date()}.")


    # -----------------------------
    # Remove Premium
    # -----------------------------
    @app.on_message(filters.command("removepremium") & filters.private)
    async def remove_premium(_, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) != 2:
            await message.reply("Usage: /removepremium user_id")
            return

        try:
            user_id = int(message.command[1])
        except ValueError:
            await message.reply("Invalid user_id")
            return

        await db.premium.delete_one({"user_id": user_id})
        await message.reply("Premium removed.")


    # -----------------------------
    # Check Premium
    # -----------------------------
    @app.on_message(filters.command("checkpremium") & filters.private)
    async def check_premium(_, message):

        if len(message.command) == 2:
            try:
                user_id = int(message.command[1])
            except ValueError:
                await message.reply("Invalid user_id")
                return
        else:
            user_id = message.from_user.id

        if await is_premium(user_id):
            await message.reply("User is Premium.")
        else:
            await message.reply("User is NOT Premium.")
