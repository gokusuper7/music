import os
import asyncio
import random

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery
from asyncio import QueueEmpty
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream

from config import get_queue
from InnexiaMusic.Cache.checker import checkerCB
from InnexiaMusic.Cache.admins import AdminRightsCheck, AdminRightsCheckCB
from InnexiaMusic.Helpers.Thumbnails import thumb_init
from InnexiaMusic.Helpers.Ytinfo import get_yt_info_id
from InnexiaMusic.Helpers.PyTgCalls import Queues, Music
from InnexiaMusic.Helpers.Changers import time_to_seconds
from InnexiaMusic.Helpers.PyTgCalls.Converter import convert
from InnexiaMusic.Helpers.PyTgCalls.Downloader import download
from InnexiaMusic import BOT_USERNAME, BOT_NAME, app, db_mem
from InnexiaMusic.Helpers.Inline import (audio_markup, primary_markup, close_key)
from InnexiaMusic.Helpers.Database import (add_active_chat, is_active_chat, remove_active_chat, is_music_playing, music_off, music_on)


loop = asyncio.get_event_loop()


@app.on_callback_query(
    filters.regex(pattern=r"^(pausecb|skipcb|stopcb|resumecb)$")
)
@AdminRightsCheckCB
@checkerCB
async def admin_risghts(_, CallbackQuery):
    global get_queue
    command = CallbackQuery.matches[0].group(1)
    if not await is_active_chat(CallbackQuery.message.chat.id):
        return await CallbackQuery.answer(
            "»  Nothing is Playing on voice-chat", show_alert=True
        )
    chat_id = CallbackQuery.message.chat.id
    if command == "pausecb":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "» Stream Already Paused.", show_alert=True
            )
        await music_off(chat_id)
        await Music.pytgcalls.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"➻ **STREAM PAUSED** ☁️\n│ \n└BY : {CallbackQuery.from_user.first_name} 🥀",
            reply_markup=audio_markup,
        )
        await CallbackQuery.answer("» Stream Paused.")
    if command == "resumecb":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "»  Nothing is paused on voice-chat", show_alert=True
            )
        await music_on(chat_id)
        await Music.pytgcalls.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"➻ **STREAM RESUMED** ✨\n│ \n└BY : {CallbackQuery.from_user.first_name} 🥀",
            reply_markup=audio_markup,
        )
        await CallbackQuery.answer("» Stream Resumed.")
    if command == "stopcb":
        try:
            Queues.clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await Music.pytgcalls.leave_group_call(chat_id)
        await CallbackQuery.message.reply_text(
            f"➻ **STREAM STOPPED** ❄\n│ \n└BY : {CallbackQuery.from_user.first_name} 🥀",
            reply_markup=close_key,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("» STREAM ENDED.")
    if command == "skipcb":
        Queues.task_done(chat_id)
        if Queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await CallbackQuery.message.reply_text(
                f"➻ **STREAM SKIPPED** 🥺\n│ \n└BY : {CallbackQuery.from_user.first_name} 🥀\n\n» NO MORE QUEUED TRACK IN {CallbackQuery.message.chat.title}, **LEAVING VOICECHAT.**",
              reply_markup=close_key,
            )
            await Music.pytgcalls.leave_group_call(chat_id)
            await CallbackQuery.message.delete()
            await CallbackQuery.answer(
                "» SKIPPED, No more track in queue."
            )
            return
        else:
            videoid = Queues.get(chat_id)["file"]
            got_queue = get_queue.get(CallbackQuery.message.chat.id)
            if got_queue:
                got_queue.pop(0)
            finxx = f"{videoid[0]}{videoid[1]}{videoid[2]}"
            aud = 0
            if str(finxx) != "raw":
                await CallbackQuery.message.delete()
                await CallbackQuery.answer(
                    "Stream skipped..."
                )
                mystic = await CallbackQuery.message.reply_text(
                    f"**DOWNLOADING NEXT TRACK FROM PLAYLIST...\n\nSTREAM SKIPPED BY {CallbackQuery.from_user.mention} !**🥀"
                )
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)                
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                await Music.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            raw_path,
                        ),
                    ),
                )
                chat_title = CallbackQuery.message.chat.title
                thumb = await thumb_init(videoid)
                buttons = primary_markup(
                    videoid,
                    CallbackQuery.from_user.id
                )
                await mystic.delete()
                mention = db_mem[videoid]["username"]
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"<b>➻ STARTED STREAMING</b>\n\n<b>✨ TITLE :</b> [{title[:40]}](https://www.youtube.com/watch?v={videoid})\n☁ <b>DURATION :</b> {duration_min} minutes\n🥀 <b>REQUESTED BY :</b> {mention}"
                    ),
                )
                os.remove(thumb)

            else:
                await CallbackQuery.message.delete()
                await CallbackQuery.answer("STREAM SKIPPED...")
                await Music.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            videoid,
                        ),
                    ),
                )
                afk = videoid
                title = db_mem[videoid]["title"]
                duration_min = db_mem[videoid]["duration"]
                duration_sec = int(time_to_seconds(duration_min))
                mention = db_mem[videoid]["username"]
                videoid = db_mem[videoid]["videoid"]
                if str(videoid) == "smex1":
                    buttons = primary_markup(
                        videoid,
                        CallbackQuery.from_user.id,
                    )
                    thumb = "InnexiaMusic/Utilities/Audio.jpeg"
                    aud = 1
                else:
                    _path_ = _path_ = (
                        (str(afk))
                        .replace("_", "", 1)
                        .replace("/", "", 1)
                        .replace(".", "", 1)
                    )
                    thumb = f"Cache/{_path_}final.png"
                    buttons = primary_markup(
                        videoid,
                        CallbackQuery.from_user.id,
                    )
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"<b>➻ STARTED STREAMING</b>\n\n<b>✨ TITLE :</b> {title[:40]}\n☁ <b>DURATION :</b> {duration_min} minutes\n🥀 <b>REQUESTED BY :</b> {mention}",
                )


@app.on_callback_query(filters.regex("close"))
async def closed(_, query: CallbackQuery):
    await query.message.delete()
    await query.answer()
