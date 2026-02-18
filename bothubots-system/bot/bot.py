from pyrogram import Client
from loader import load_core, load_clones
from config import Config
import asyncio

# Main bot instance
app = Client(
    "main_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot.plugins")
)

@app.on_start()
async def start_bot(client):
    await load_core(client)
    await load_clones(client)

if __name__ == "__main__":
    app.run()
