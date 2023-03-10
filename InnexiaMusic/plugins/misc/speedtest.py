import os
import wget
import speedtest
import asyncio

from PIL import Image
from pyrogram.types import Message
from pyrogram import filters, Client
from strings import get_command
from InnexiaMusic import app
from InnexiaMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")




@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def run_speedtest(_, message):
    userid = message.from_user.id
    m = await message.reply_text("Running Speed test")
    test = speedtest.Speedtest()
    test.get_best_server()
    await m.edit("🔥 __running download speedtest__")
    test.download()
    await m.edit("🔥 __running upload speedtest__")
    test.upload()
    test.results.share()
    result = test.results.dict()
    await m.edit("💠 Sharing Speedtest")
    output = f"""💡 **SpeedTest Results**
    
<u>**Client:**</u>
**ISP:** {result['client']['isp']}
**Country:** {result['client']['country']}
  
<u>**Server:**</u>
**Name:** {result['server']['name']}
**Country:** {result['server']['country']}, {result['server']['cc']}
**Sponsor:** {result['server']['sponsor']}
**Latency:** {result['server']['latency']}  
⚡ **Ping:** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, 
        photo=result["share"], 
        caption=output
    )
    await m.delete()
