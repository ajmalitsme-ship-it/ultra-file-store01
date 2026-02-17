import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.database import db
from core.storage import Storage
from core.config import (
    WEB_APP_URL,
    PREMIUM_FILE_LIMIT_MB,
    FREE_FILE_LIMIT_MB
)
from core.rate_limit import check_rate
from bot.premium import is_premium


storage = Storage()


def register_file_store(app):

    @app.on_message(
        filters.private
        & (filters.document | filters.video)
        & ~filters.command(["startbatch", "endbatch"])
    )
    async def store_file(client, message):

        user_id = message.from_user.id

        # ----------------------------
        # Rate Limit
        # ----------------------------
        if not check_rate(f"upload:{user_id}", limit=15, period=60):
            await message.reply("Upload limit reached. Try again later.")
            return

        # ----------------------------
        # Detect File Object
        # ----------------------------
        file_obj = message.document or message.video

        file_size_mb = file_obj.file_size / (1024 * 1024)

        # ----------------------------
        # Premium Check
        # ----------------------------
        premium = await is_premium(user_id)

        if premium:
            if file_size_mb > PREMIUM_FILE_LIMIT_MB:
                await message.reply(
                    f"Premium limit exceeded. Max {PREMIUM_FILE_LIMIT_MB} MB allowed."
                )
                return
        else:
            if file_size_mb > FREE_FILE_LIMIT_MB:
                await message.reply(
                    f"Free limit exceeded. Max {FREE_FILE_LIMIT_MB} MB allowed."
                )
                return

        # ----------------------------
        # Download File
        # ----------------------------
        try:
            file_path = await message.download()
        except Exception:
            await message.reply("Failed to download file.")
            return

        # ----------------------------
        # Save To Storage
        # ----------------------------
        file_id, saved_path = await storage.save(file_path)

        # ----------------------------
        # Insert To DB
        # ----------------------------
        await db.files.insert_one({
            "file_id": file_id,
            "file_name": file_obj.file_name,
            "mime_type": file_obj.mime_type,
            "file_size": file_obj.file_size,
            "path": saved_path,
            "uploader": user_id,
            "downloads": 0,
            "created_at": datetime.datetime.utcnow()
        })

        # ----------------------------
        # Generate Button
        # ----------------------------
        button = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "🔗 Get Link",
                    callback_data=f"get_{file_id}"
                )
            ]]
        )

        # ----------------------------
        # Reply
        # ----------------------------
        await message.reply(
            "✅ File Stored Successfully",
            reply_markup=button
              )
