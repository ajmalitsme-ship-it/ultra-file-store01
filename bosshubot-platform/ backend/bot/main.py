import asyncio
from bot.loader import load_bots, active_bots
from bot.admin import register_admin
from bot.file_store import register_file_store
from bot.callbacks import register_callbacks

async def main():

    await load_bots()

    for bot_id, app in active_bots.items():
        register_admin(app, bot_id)
        register_file_store(app, bot_id)
        register_callbacks(app, bot_id)

    await asyncio.gather(*(app.idle() for app in active_bots.values()))

asyncio.run(main())
