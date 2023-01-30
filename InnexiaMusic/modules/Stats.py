
import os
import re
import json
import uuid
import time
import psutil
import socket
import logging
import asyncio
import platform

from datetime import datetime
from sys import version as pyver
from pymongo import MongoClient

from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pyrogram.types import Message
from InnexiaMusic import (BOT_NAME, SUDO_USERS, app, Ass, StartTime, MONGO_DB_URI)
from InnexiaMusic.Helpers.Database import get_gbans_count, get_served_chats, get_served_users
from InnexiaMusic.Helpers.Inline import stats_f, stats_b
from InnexiaMusic.Modules import ALL_MODULES
from InnexiaMusic.Helpers.ping import get_readable_time




@app.on_message(filters.command(["stats", "getstats"]) & ~filters.edited)
async def gstats(_, message):
    try:
        await message.delete()
    except:
        pass
    hehe = await message.reply_photo(
        photo="InnexiaMusic/Utilities/Stats.jpeg", caption=f"**» Please wait...\n\n• Getting {BOT_NAME} stats...**"
    )
    groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0
    async for i in Ass.iter_dialogs():
        t = i.chat.type
        total_ub += 1
        if t in ["supergroup", "group"]:
            groups_ub += 1
        elif t == "channel":
            channels_ub += 1
        elif t == "bot":
            bots_ub += 1
        elif t == "private":
            privates_ub += 1
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    blocked = await get_gbans_count()
    sudoers = len(SUDO_USERS)
    mod = len(ALL_MODULES)
    smex = f"""
➻ <u>**{BOT_NAME} ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs :**</u>
• **ᴍᴏᴅᴜʟᴇs :** {mod}
• **ɢʙᴀɴɴᴇᴅ :** {blocked}
• **sᴜᴅᴏᴇʀs :** {sudoers}
• **ᴄʜᴀᴛs :** {served_chats}
• **ᴜsᴇʀs :** {served_users}
➻ <u>**{BOT_NAME} ᴀssɪsᴛᴀɴᴛ sᴛᴀᴛs :**</u>
• **ᴛᴏᴛᴀʟ :** {total_ub}
• **ɢʀᴏᴜᴩs :** {groups_ub}
• **ᴄʜᴀɴɴᴇʟs :** {channels_ub}
• **ʙᴏᴛs :** {bots_ub}
• **ᴜsᴇʀs :** {privates_ub}
"""
    await hehe.edit_text(smex)
