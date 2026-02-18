from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
from pyrogram import Client
import asyncio

async def load_core(client):
    mongo = AsyncIOMotorClient(Config.MONGO_URI)
    db = mongo["filestore"]

    client.mongo = mongo
    client.db = db

    client.users = db["users"]
    client.settings = db["settings"]
    client.files = db["files"]
    client.clones = db["clones"]

    # Default settings
    if not await client.settings.find_one({}):
        await client.settings.insert_one({
            "force_sub": True,
            "shortlink": True,
            "auto_delete": 600,
            "signed_stream": True,
            "db_channels": [Config.DB_CHANNEL]
        })

    print("Core system loaded.")

# -----------------------------------
# Clone Loader
# -----------------------------------

async def load_clones(main_client):
    clones = await main_client.clones.find({"active": True}).to_list(None)

    for clone in clones:
        try:
            clone_app = Client(
                f"clone_{clone['_id']}",
                api_id=Config.API_ID,
                api_hash=Config.API_HASH,
                bot_token=clone["token"],
                plugins=dict(root="bot.plugins")
            )

            await clone_app.start()
            await load_core(clone_app)

            print(f"Clone started: {clone['token']}")

        except Exception as e:
            print(f"Clone failed: {e}")
