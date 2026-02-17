from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.database import db
from core.storage import LocalStorage
from core.config_service import get_web_url
import datetime

storage = LocalStorage()

def register_file_store(app, bot_id):

    @app.on_message(filters.private & (filters.document | filters.video))
    async def save_file(client, message):

        file_path = await message.download()
        file_id, path = await storage.save(file_path)

        await db.files.insert_one({
            "file_id": file_id,
            "bot_id": bot_id,
            "file_name": message.document.file_name,
            "mime_type": message.document.mime_type,
            "path": path,
            "created_at": datetime.datetime.utcnow()
        })

        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Get Link", callback_data=f"get_{file_id}")]]
        )

        await message.reply("Stored Successfully", reply_markup=buttons)
