
import asyncio
import speedtest

from pyrogram import filters
from InnexiaMusic import app, SUDO_USERS


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("**⇆ Running Download speedtest...**")
        test.download()
        m = m.edit("**⇆ Running Upload speedtest...**")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("**↻ Sharing speedtest result...**")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(["speedtest", "sptest", "spt"]) & filters.user(SUDO_USERS))
async def speedtest_function(client, message):
    m = await message.reply_text("**» Running Speedtest...**")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""✯ **SPEEDTEST RESULT** ✯
    
<u>**❥͜͡Client :**</u>
**» __ISP :__** {result['client']['isp']}
**» __COUNTRY :__** {result['client']['country']}
  
<u>**❥͜͡Server :**</u>
**» __NAME :__** {result['server']['name']}
**» __COUNTRY :__** {result['server']['country']}, {result['server']['cc']}
**» __SPONSOR :__** {result['server']['sponsor']}
**» __LATENCY :__** {result['server']['latency']}  
**» __PING :__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, 
        photo=result["share"], 
        caption=output
    )
    await m.delete()
