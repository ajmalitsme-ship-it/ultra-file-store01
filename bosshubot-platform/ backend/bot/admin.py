from pyrogram import filters
from core.database import db
from core.permissions import is_admin

def register_admin(app, bot_id):

    @app.on_message(filters.command("addadmin"))
    async def add_admin(client, message):
        if not await is_admin(message.from_user.id, bot_id):
            return
        
        user_id = int(message.text.split()[1])

        await db.bots.update_one(
            {"bot_id": bot_id},
            {"$addToSet": {"admins": user_id}}
        )

        await message.reply("Admin Added")

    @app.on_message(filters.command("removeadmin"))
    async def remove_admin(client, message):
        if not await is_admin(message.from_user.id, bot_id):
            return
        
        user_id = int(message.text.split()[1])

        await db.bots.update_one(
            {"bot_id": bot_id},
            {"$pull": {"admins": user_id}}
        )

        await message.reply("Admin Removed")
