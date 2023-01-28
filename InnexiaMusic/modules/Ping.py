import os
import time
import config
from datetime import datetime

import psutil
from pyrogram import filters
from pyrogram.types import Message

from InnexiaMusic.Helpers.Inline import ping_ig
from InnexiaMusic.Helpers.Ping import get_readable_time
from InnexiaMusic import BOT_USERNAME, BOT_NAME, app, StartTime

async def _ping():
    uptime = int(time.time() - StartTime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    AsuX = f"""
✨ UPTIME : {get_readable_time((uptime))}
☁ CPU : {cpu}%
❄ RAM : {mem}%
💠 DISK : {disk}%"""
    return _

@app.on_message(filters.command(["ping", f"ping@{BOT_USERNAME}"]))
async def ping(_, message):
    hmm = await message.reply_photo(
        photo=config.PING_IMG,
        caption="**» Pong!",
    )
    hehe = await _ping()
    start = datetime.now()
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await hmm.edit_text(
        f"**Pong!**\n`⚡{resp} ms`\n\n<b><u>{MUSIC_BOT_NAME} System Stats:</u></b>{uptime}", 
        reply_markup=ping_ig,
    )
