from pyrogram import Client
from bot.config import Config

app = Client(
    "bothubots",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot/plugins")
)

app.run()
