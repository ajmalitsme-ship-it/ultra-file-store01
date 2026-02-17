from pyrogram import filters
from core.database import db
from core.permissions import is_admin

def register_force_sub(app, bot_id):

    @app.on_message(filters.command("addforcesub"))
    async def add_force(client, message):
        if not await is_admin(message.from_user.id, bot_id):
            return

        channel_id = int(message.text.split()[1])

        await db.force_channels.insert_one({
            "bot_id": bot_id,
            "channel_id": channel_id
        })

        await message.reply("ForceSub Added")

    @app.on_message(filters.command("removeforcesub"))
    async def remove_force(client, message):
        if not await is_admin(message.from_user.id, bot_id):
            return

        channel_id = int(message.text.split()[1])

        await db.force_channels.delete_one({
            "
