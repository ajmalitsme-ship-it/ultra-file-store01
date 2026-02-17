from pyrogram import filters
from pyrogram.errors import UserNotParticipant

from core.database import db
from core.config import FORCE_SUB_ENABLED
from core.permissions import is_admin


def register_force_sub(app):

    # ==============================
    # Add ForceSub Channel
    # ==============================
    @app.on_message(filters.command("addforcesub") & filters.private)
    async def add_force(_, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) != 2:
            await message.reply("Usage: /addforcesub channel_id")
            return

        try:
            channel_id = int(message.command[1])
        except ValueError:
            await message.reply("Invalid channel_id")
            return

        await db.force_sub.update_one(
            {"channel_id": channel_id},
            {"$set": {"channel_id": channel_id}},
            upsert=True
        )

        await message.reply("ForceSub channel added.")


    # ==============================
    # Remove ForceSub Channel
    # ==============================
    @app.on_message(filters.command("removeforcesub") & filters.private)
    async def remove_force(_, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) != 2:
            await message.reply("Usage: /removeforcesub channel_id")
            return

        try:
            channel_id = int(message.command[1])
        except ValueError:
            await message.reply("Invalid channel_id")
            return

        await db.force_sub.delete_one({"channel_id": channel_id})

        await message.reply("ForceSub channel removed.")


    # ==============================
    # List ForceSub Channels
    # ==============================
    @app.on_message(filters.command("listforcesub") & filters.private)
    async def list_force(_, message):

        if not await is_admin(message.from_user.id):
            return

        channels = []
        async for ch in db.force_sub.find():
            channels.append(str(ch["channel_id"]))

        if not channels:
            await message.reply("No ForceSub channels found.")
            return

        text = "ForceSub Channels:\n\n" + "\n".join(channels)
        await message.reply(text)


    # ==============================
    # ForceSub Check (Non-blocking)
    # ==============================
    @app.on_message(filters.private & ~filters.command([
        "addforcesub",
        "removeforcesub",
        "listforcesub"
    ]))
    async def check_force(client, message):

        if not FORCE_SUB_ENABLED or not message.from_user:
            return

        async for ch in db.force_sub.find():
            try:
                await client.get_chat_member(
                    ch["channel_id"],
                    message.from_user.id
                )
            except UserNotParticipant:
                await message.reply(
                    "⚠️ You must join required channels before using this bot."
                )
                return
            except Exception:
                # Bot may not be admin in channel
                continue
