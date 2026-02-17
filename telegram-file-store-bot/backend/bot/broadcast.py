import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait

from core.permissions import is_admin
from core.database import db
from core.rate_limit import check_rate


def register_broadcast(app):

    @app.on_message(filters.command("broadcast") & filters.private)
    async def broadcast_handler(client, message):

        user_id = message.from_user.id

        # -----------------------------
        # Admin Check
        # -----------------------------
        if not await is_admin(user_id):
            return

        # -----------------------------
        # Rate Limit Protection
        # -----------------------------
        if not check_rate(f"broadcast:{user_id}", limit=2, period=300):
            await message.reply("Broadcast limit reached. Try later.")
            return

        # -----------------------------
        # Get Broadcast Content
        # -----------------------------
        if message.reply_to_message:
            broadcast_message = message.reply_to_message
        else:
            if len(message.command) < 2:
                await message.reply(
                    "Usage:\n"
                    "Reply to a message with /broadcast\n"
                    "OR\n"
                    "/broadcast your text here"
                )
                return

            text = message.text.split(None, 1)[1]
            broadcast_message = text

        await message.reply("📢 Broadcast started...")

        total = 0
        success = 0
        failed = 0

        users_cursor = db.users.find()

        async for user in users_cursor:
            total += 1
            try:
                if isinstance(broadcast_message, str):
                    await client.send_message(
                        user["user_id"],
                        broadcast_message
                    )
                else:
                    await broadcast_message.copy(user["user_id"])

                success += 1
                await asyncio.sleep(0.2)  # Anti flood delay

            except FloodWait as e:
                await asyncio.sleep(e.value)
                continue
            except Exception:
                failed += 1

        # -----------------------------
        # Final Report
        # -----------------------------
        await message.reply(
            f"📊 Broadcast Completed\n\n"
            f"Total Users: {total}\n"
            f"Success: {success}\n"
            f"Failed: {failed}"
  )
