from pyrogram import Client, filters
from config import BOT_TOKEN, API_ID, API_HASH, WEB_DOMAIN
from database import save_file, add_user, is_premium
from forcejoin import check_force_join
from admin import admin_filter, stats_cmd, broadcast_cmd
from payments import buy_premium_buttons, handle_paid_callback, admin_verify

app = Client("filestore", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.private)
async def track_user(_, m):
    if m.from_user:
        add_user(m.from_user.id)


@app.on_message(filters.command("premium"))
async def premium_cmd(_, m):
    await m.reply("Buy Premium ₹10 / 30 days", reply_markup=buy_premium_buttons(m.from_user.id))


@app.on_callback_query(filters.regex("^paid_"))
async def paid_callback(client, q):
    await handle_paid_callback(client, q)


@app.on_message(filters.command("verify") & admin_filter())
async def verify_cmd(client, m):
    await admin_verify(client, m)


@app.on_message(filters.document)
async def save_doc(_, m):
    if not await check_force_join(app, m):
        return

    if not is_premium(m.from_user.id):
        return await m.reply("Premium required. Use /premium")

    code = await save_file(m.document.file_id)
    await m.reply(f"{WEB_DOMAIN}/watch/{code}")


@app.on_message(filters.command("stats") & admin_filter())
async def _s(_, m):
    await stats_cmd(m)


@app.on_message(filters.command("broadcast") & admin_filter())
async def _b(client, m):
    await broadcast_cmd(client, m)


app.run()
