
import os
import asyncio

from config import get_queue
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from InnexiaMusic import app, db_mem
from InnexiaMusic.Helpers.Database import is_active_chat
from InnexiaMusic.Helpers.Inline import primary_markup



@app.on_callback_query(filters.regex("pr_go_back_timer"))
async def pr_go_back_timer(_, CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            buttons = primary_markup(videoid, user_id)
            await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
   

@app.on_callback_query(filters.regex("timer_checkup_markup"))
async def timer_checkup_markup(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            return await CallbackQuery.answer(
                f"REMAINING {dur_left} OUT OF {duration_min} minutes.",
                show_alert=True,
            )
        return await CallbackQuery.answer(f"Nothing is playing...", show_alert=True)
    else:
        return await CallbackQuery.answer(
            f"No Active voice chat Found.", show_alert=True
        )


@app.on_message(filters.command("queue"))
async def activevc(_, message: Message):
    global get_queue
    if await is_active_chat(message.chat.id):
        mystic = await message.reply_text("**» Please wait, Getting Queue...**")
        dur_left = db_mem[message.chat.id]["left"]
        duration_min = db_mem[message.chat.id]["total"]
        got_queue = get_queue.get(message.chat.id)
        if not got_queue:
            await mystic.edit("**» QUEUE EMPTY.**")
        fetched = []
        for get in got_queue:
            fetched.append(get)

        current_playing = fetched[0][0]
        user_name = fetched[0][1]

        msg = "**QUEUED LIST**\n\n"
        msg += "**PLAYINH :**"
        msg += "\n‣" + current_playing[:30]
        msg += f"\n   ╚ BY : {user_name}"
        msg += f"\n   ╚ DURATION : REMAINING `{dur_left}` OUT OF`{duration_min}` minutes."
        fetched.pop(0)
        if fetched:
            msg += "\n\n"
            msg += "**NEXT IN QUEUE:**"
            for song in fetched:
                name = song[0][:30]
                usr = song[1]
                dur = song[2]
                msg += f"\n❚❚ {name}"
                msg += f"\n   ╠ DURATION : {dur}"
                msg += f"\n   ╚ REQUESTED BY: {usr}\n"
        if len(msg) > 4096:
            await mystic.delete()
            filename = "queue.txt"
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(msg.strip()))
            await message.reply_document(
                document=filename,
                caption="**QUEUED LIST**",
                quote=False,
            )
            os.remove(filename)
        else:
            await mystic.edit(msg)
    else:
        await message.reply_text(f"**» QUEUE EMPTY.**")
