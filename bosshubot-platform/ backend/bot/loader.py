from pyrogram import Client
from core.database import db
from core.config import API_ID, API_HASH

active_bots = {}

async def load_bots():

    bots = db.bots.find({"status": "active"})

    async for bot_data in bots:

        app = Client(
            name=str(bot_data["bot_id"]),
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=bot_data["bot_token"]
        )

        await app.start()
        active_bots[bot_data["bot_id"]] = app
