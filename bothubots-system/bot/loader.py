from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
from pyrogram import Client

async def load_core(client):
    mongo = AsyncIOMotorClient(Config.MONGO_URI)
    db = mongo["filestore"]

    client.db = db
    client.users = db["users"]
    client.files = db["files"]
    client.settings = db["settings"]
    client.clones = db["clones"]

    if not await client.settings.find_one({}):
        await client.settings.insert_one({
            "force_sub": True,
            "shortlink": True,
            "auto_delete": 600,
            "db_channels": [Config.MAIN_DB_CHANNEL]
        })

async def load_clones(main_client):
    clones = await main_client.clones.find({"active": True}).to_list(None)

    for clone in clones:
        clone_app = Client(
            f"clone_{clone['_id']}",
            api_id=main_client.api_id,
            api_hash=main_client.api_hash,
            bot_token=clone["token"],
            plugins=dict(root="bot.plugins")
        )
        await clone_app.start()
        await load_core(clone_app)
