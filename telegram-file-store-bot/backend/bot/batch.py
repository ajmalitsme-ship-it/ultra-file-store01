import uuid
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

# In-memory batch sessions
batch_sessions = {}


def register_batch(app):

    # ==============================
    # START BATCH
    # ==============================
    @app.on_message(filters.command("startbatch"))
    async def start_batch(_, message):

        user_id = message.from_user.id

        if user_id in batch_sessions:
            await message.reply("You already have an active batch.")
            return

        batch_id = str(uuid.uuid4())

        batch_sessions[user_id] = {
            "batch_id": batch_id,
            "files": []
        }

        await db.batches.insert_one({
            "batch_id": batch_id,
            "uploader": user_id,
            "files": [],
            "created_at": datetime.datetime.utcnow()
        })

        await message.reply("📦 Batch started. Send files now.\nUse /endbatch when done.")


    # ==============================
    # ADD FILE TO BATCH
    # ==============================
    @app.on_message(
        filters.private
        & (filters.document | filters.video)
        & ~filters.command(["startbatch", "endbatch"])
    )
    async def add_file_to_batch(client, message):

        user_id = message.from_user.id

        if user_id not in batch_sessions:
            return  # Let file_store.py handle normal uploads

        if not check_rate(f"batch_upload:{user_id}", limit=20, period=60):
            await message.reply("Batch upload limit reached. Try later.")
            return

        file_obj = message.document or message.video
        file_size_mb = file_obj.file_size / (1024 * 1024)

        premium = await is_premium(user_id)

        if premium:
            if file_size_mb > PREMIUM_FILE_LIMIT_MB:
                await message.reply(
                    f"Premium limit exceeded ({PREMIUM_FILE_LIMIT_MB} MB)"
                )
                return
        else:
            if file_size_mb > FREE_FILE_LIMIT_MB:
                await message.reply(
                    f"Free limit exceeded ({FREE_FILE_LIMIT_MB} MB)"
                )
                return

        try:
            file_path = await message.download()
        except Exception:
            await message.reply("Failed to download file.")
            return

        file_id, saved_path = await storage.save(file_path)

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

        # Update batch DB
        await db.batches.update_one(
            {"batch_id": batch_sessions[user_id]["batch_id"]},
            {"$push": {"files": file_id}}
        )

        batch_sessions[user_id]["files"].append(file_id)

        await message.reply("✅ File added to batch.")


    # ==============================
    # END BATCH
    # ==============================
    @app.on_message(filters.command("endbatch"))
    async def end_batch(_, message):

        user_id = message.from_user.id

        if user_id not in batch_sessions:
            await message.reply("No active batch found.")
            return

        batch_data = batch_sessions[user_id]

        if not batch_data["files"]:
            await message.reply("Batch is empty. Nothing saved.")
            del batch_sessions[user_id]
            return

        batch_id = batch_data["batch_id"]

        del batch_sessions[user_id]

        batch_link = f"{WEB_APP_URL}/batch/{batch_id}"

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📂 Open Batch", url=batch_link)]]
        )

        await message.reply(
            "📦 Batch completed successfully.",
            reply_markup=button
)
