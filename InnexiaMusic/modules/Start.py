
import time
import config
import asyncio
from typing import Dict, List, Union

from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message)

from InnexiaMusic import ASSID, BOT_NAME, BOT_USERNAME, OWNER_ID, SUDO_USERS, F_OWNER, app
from InnexiaMusic.Helpers.Database import (add_served_chat, add_served_user, is_served_chat, remove_active_chat)
from InnexiaMusic.Cache.permission import PermissionCheck
from InnexiaMusic.Helpers.Inline import start_pannel


welcome_group = 2



@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id == ASSID:
                return await remove_active_chat(chat_id)
            elif member.id in OWNER_ID:
                return await message.reply_text(
                    f"**» the owner of  {BOT_NAME} just joined the chat.**\n\n➻ owner : [{member.mention}] 🥀"
                )
            elif member.id in SUDO_USERS:
                return await message.reply_text(
                    f"**» a sudo user of {BOT_NAME} just joined the chat.**\n\n➻ sudoer : [{member.mention}] 🥀"
                )
                return
        except:
            return
