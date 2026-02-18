from pyrogram import Client
from config import Config
from loader import load_core, load_clones

app = Client(
    "main_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot.plugins")
)

@app.on_start()
async def startup(client):
    await load_core(client)
    await load_clones(client)

app.run()
