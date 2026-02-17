import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait

from core.permissions import is_admin


def register_forward(app):

    # ==============================
    # Forward Range
    # ==============================
    @app.on_message(filters.command("forwardrange") & filters.private)
    async def forward_range(client, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) != 4:
            await message.reply(
                "Usage:\n"
                "/forwardrange channel_id first_msg_id last_msg_id"
            )
            return

        try:
            channel_id = int(message.command[1])
            first_id = int(message.command[2])
            last_id = int(message.command[3])
        except ValueError:
            await message.reply("Invalid input.")
            return

        if first_id > last_id:
            await message.reply("First ID cannot be greater than Last ID.")
            return

        await message.reply("Forwarding started...")

        count = 0

        for msg_id in range(first_id, last_id + 1):
            try:
                await client.forward_messages(
                    chat_id=message.chat.id,
                    from_chat_id=channel_id,
                    message_ids=msg_id
                )
                count += 1
                await asyncio.sleep(0.2)

            except FloodWait as e:
                await asyncio.sleep(e.value)
                continue
            except Exception:
                continue

        await message.reply(f"Forward completed. {count} messages forwarded.")


    # ==============================
    # Forward Single Message
    # ==============================
    @app.on_message(filters.command("forward") & filters.private)
    async def forward_single(client, message):

        if not await is_admin(message.from_user.id):
            return

        if len(message.command) != 3:
            await message.reply(
                "Usage:\n"
                "/forward channel_id message_id"
            )
            return

        try:
            channel_id = int(message.command[1])
            msg_id = int(message.command[2])
        except ValueError:
            await message.reply("Invalid input.")
            return

        try:
            await client.forward_messages(
                chat_id=message.chat.id,
                from_chat_id=channel_id,
                message_ids=msg_id
            )
            await message.reply("Message forwarded successfully.")
        except Exception:
            await message.reply("Failed to forward message.")
