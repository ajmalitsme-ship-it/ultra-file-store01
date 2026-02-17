from pyrogram import filters
from core.permissions import is_admin
from core.database import db
from core.config import OWNER_ID


def register_admin(app):

    # ==============================
    # Add Admin
    # ==============================
    @app.on_message(filters.command("addadmin"))
    async def add_admin(_, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) < 2:
            await message.reply("Usage: /addadmin user_id")
            return

        try:
            user_id = int(message.command[1])
        except ValueError:
            await message.reply("Invalid user_id")
            return

        await db.admins.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id}},
            upsert=True
        )

        await message.reply(f"Admin {user_id} added successfully")


    # ==============================
    # Remove Admin
    # ==============================
    @app.on_message(filters.command("removeadmin"))
    async def remove_admin(_, message):

        if message.from_user.id != OWNER_ID:
            return

        if len(message.command) < 2:
            await message.reply("Usage: /removeadmin user_id")
            return

        try:
            user_id = int(message.command[1])
        except ValueError:
            await message.reply("Invalid user_id")
            return

        await db.admins.delete_one({"user_id": user_id})
        await message.reply(f"Admin {user_id} removed")


    # ==============================
    # List Admins
    # ==============================
    @app.on_message(filters.command("listadmins"))
    async def list_admins(_, message):

        if not await is_admin(message.from_user.id):
            return

        admins = []
        async for admin in db.admins.find():
            admins.append(str(admin["user_id"]))

        if not admins:
            await message.reply("No admins found.")
            return

        text = "Admins:\n\n" + "\n".join(admins)
        await message.reply(text)


    # ==============================
    # Add ForceSub Channel
    # ==============================
    @app.on_message(filters.command("addforcesub"))
    async def add_force_sub(_, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) < 2:
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

        await message.reply(f"ForceSub channel {channel_id} added")


    # ==============================
    # Remove ForceSub Channel
    # ==============================
    @app.on_message(filters.command("removeforcesub"))
    async def remove_force_sub(_, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) < 2:
            await message.reply("Usage: /removeforcesub channel_id")
            return

        try:
            channel_id = int(message.command[1])
        except ValueError:
            await message.reply("Invalid channel_id")
            return

        await db.force_sub.delete_one({"channel_id": channel_id})
        await message.reply(f"ForceSub channel {channel_id} removed")


    # ==============================
    # List ForceSub Channels
    # ==============================
    @app.on_message(filters.command("listforcesub"))
    async def list_force_sub(_, message):

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
