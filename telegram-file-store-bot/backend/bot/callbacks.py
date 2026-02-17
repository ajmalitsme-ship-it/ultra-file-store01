from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.database import db
from core.config import WEB_APP_URL


def register_callbacks(app):

    # =====================================
    # File Link Callback
    # =====================================
    @app.on_callback_query(filters.regex("^get_"))
    async def file_link_callback(_, callback_query):

        file_id = callback_query.data.split("_", 1)[1]

        file = await db.files.find_one({"file_id": file_id})

        if not file:
            await callback_query.message.reply("File not found.")
            return

        # Increment download counter
        await db.files.update_one(
            {"file_id": file_id},
            {"$inc": {"downloads": 1}}
        )

        link = f"{WEB_APP_URL}/watch/{file_id}"

        await callback_query.message.reply(
            f"🔗 Download Link:\n{link}"
        )

        await callback_query.answer()


    # =====================================
    # Batch Link Callback (Optional Use)
    # =====================================
    @app.on_callback_query(filters.regex("^batch_"))
    async def batch_link_callback(_, callback_query):

        batch_id = callback_query.data.split("_", 1)[1]

        batch = await db.batches.find_one({"batch_id": batch_id})

        if not batch:
            await callback_query.message.reply("Batch not found.")
            return

        link = f"{WEB_APP_URL}/batch/{batch_id}"

        await callback_query.message.reply(
            f"📦 Batch Link:\n{link}"
        )

        await callback_query.answer()
