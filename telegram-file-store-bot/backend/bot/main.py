import asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    MONGO_URI
)

from core.database import db

from bot.admin import register_admin
from bot.file_store import register_file_store
from bot.batch import register_batch
from bot.broadcast import register_broadcast
from bot.forward import register_forward
from bot.force_sub import register_force_sub
from bot.callbacks import register_callbacks
from bot.premium import register_premium


# ==============================
# Create Bot Client
# ==============================

app = Client(
    "telegram-file-store",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# ==============================
# Auto Save Users
# ==============================

@app.on_message(filters.private & filters.incoming)
async def auto_save_user(_, message):
    if not message.from_user:
        return

    await db.users.update_one(
        {"user_id": message.from_user.id},
        {
            "$set": {
                "user_id": message.from_user.id,
                "username": message.from_user.username,
                "first_name": message.from_user.first_name
            }
        },
        upsert=True
    )


# ==============================
# Initialize DB Indexes
# ==============================

async def init_indexes():
    await db.users.create_index("user_id", unique=True)
    await db.admins.create_index("user_id", unique=True)
    await db.files.create_index("file_id", unique=True)
    await db.force_sub.create_index("channel_id", unique=True)
    await db.premium.create_index("user_id", unique=True)
    await db.batches.create_index("batch_id", unique=True)


# ==============================
# Register All Modules
# ==============================

def register_modules(client: Client):
    register_admin(client)
    register_force_sub(client)
    register_file_store(client)
    register_batch(client)
    register_broadcast(client)
    register_forward(client)
    register_callbacks(client)
    register_premium(client)


# ==============================
# Startup
# ==============================

async def main():
    await init_indexes()
    register_modules(app)
    await app.start()
    print("Bot Started Successfully")
    await idle()


# ==============================
# Run
# ==============================

if __name__ == "__main__":
    from pyrogram import idle
    asyncio.run(main())
