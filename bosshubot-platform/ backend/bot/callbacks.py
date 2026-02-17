from pyrogram import filters
from core.config_service import get_web_url

def register_callbacks(app, bot_id):

    @app.on_callback_query(filters.regex("^get_"))
    async def send_link(client, callback_query):

        file_id = callback_query.data.split("_")[1]

        web_url = await get_web_url(bot_id)
        link = f"{web_url}/watch/{file_id}"

        await callback_query.message.reply(link)
