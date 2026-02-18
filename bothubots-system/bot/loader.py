"""
Loader Module
-------------

Responsible for:

- Initializing database
- Attaching DB to client
- Preparing default settings
- Preparing global bot attributes
- Pre-loading configuration flags

This keeps bot.py clean and production-ready.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import Config
from bot.helper.database import Database


async def load_bot(client):
    """
    Initialize and attach all required services to client.
    """

    # -------------------------
    # MongoDB Initialization
    # -------------------------
    mongo_client = AsyncIOMotorClient(Config.MONGO_URI)

    client.mongo = mongo_client
    client.db = mongo_client["bothubots"]

    # Attach collections for quick access
    client.users = client.db["users"]
    client.files = client.db["files"]
    client.requests = client.db["requests"]
    client.settings = client.db["settings"]

    # -------------------------
    # Ensure Default Settings
    # -------------------------
    settings = await client.settings.find_one({})

    if not settings:
        await client.settings.insert_one({
            "force_sub": False,
            "required_channels": [],
            "premium_bypass": True,
            "request_mode": "normal",  # normal / premium
            "shortlink": True,
            "auto_delete": 600
        })

    # -------------------------
    # Attach Runtime Flags
    # -------------------------
    settings = await client.settings.find_one({})

    client.force_sub_enabled = settings.get("force_sub", False)
    client.premium_bypass = settings.get("premium_bypass", True)
    client.request_mode = settings.get("request_mode", "normal")
    client.shortlink_enabled = settings.get("shortlink", True)
    client.auto_delete_time = settings.get("auto_delete", 600)

    # -------------------------
    # Attach Admin List
    # -------------------------
    client.admins = [Config.OWNER_ID]

    # -------------------------
    # Streaming Base Domain
    # -------------------------
    client.domain = Config.DOMAIN

    print("✅ Bothubots system loaded successfully.")
