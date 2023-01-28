
import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from InnexiaMusic import app, Ass, BOT_NAME, SUDO_USERS
from InnexiaMusic.Helpers.Database import get_active_chats


@app.on_message(filters.command(["activevc", "activevoice"]) & filters.user(SUDO_USERS))
async def activevc(_, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"**ERROR :** {e}")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "ᴩʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴩ 😗"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n\n"
        j += 1
    if not text:
        await message.reply_text(f"**» NO ACTIVE VOICE-CHAT**")
    else:
        await message.reply_text(
            f"**» ACTIVE VOICE-CHAT LIST:**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["join", "ujoin]) & filters.user(SUDO_USERS))
async def assjoin(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**EXAMPLE :**\n/ujoin [CHAT USERNAME OR CHAT ID]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await Ass.join_chat(chat)
    except Exception as e:
        await message.reply_text(f"FAULED.\n\n**REASON :** {e}")
        return
    await message.reply_text("**» successfully joined that chat.**")


@app.on_message(filters.command(["leavebot", "leave"]) & filters.user(SUDO_USERS))
async def botl(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**EXAMPLE :**\n/leavebot [CHAT USERNAME OR CHAT ID]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await app.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"FAILED\n**REASON :** {e}")
        print(e)
        return
    await message.reply_text("**» SUCCESSFULLY JOINED THE CHAT.**")


@app.on_message(filters.command(["uleave", "assleave", "userbotleave", "leaveass"]) & filters.user(SUDO_USERS))
async def assleave(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**EXAMPLE :**\n/uleave [CHAT USERNAME OR CHAT ID]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await Ass.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"FAILED\n**REASON :** {e}")
        return
    await message.reply_text("**» ASSISTANT SUCCESSFULLY LEFT THE CHAT.**")
