
import os
import config
import asyncio

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from InnexiaMusic import BOT_ID, BOT_NAME, SUDO_USERS, app
from InnexiaMusic.Helpers.Database import (add_gban_user, get_served_chats, is_gbanned_user, remove_gban_user)




@app.on_message(filters.command("gban") & filters.user(SUDO_USERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**EXAMPLE :**\n/gban [USERNAME|USER ID]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "**» YOU CAN'T GBAN YOURSELF!**"
            )
        elif user.id == BOT_ID:
            await message.reply_text("» I Can't Gban Myself Lol!")
        elif user.id in SUDO_USERS:
            await message.reply_text("» Abe Lode Tu thoda sa bhen ka loda hai kya 🤣🤣!")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**GLOBALLY BANNING {user.mention}**\n\nEXPECTED TIME: {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
**GLOBAL BAN {BOT_NAME}**
**• CHAT :** {message.chat.title} [`{message.chat.id}`]
**• SUDOER :** {from_user.mention}
**• USER :** {user.mention}
**•USER ID:** `{user.id}`
**• BANNED IN :** {number_of_chats} CHATS"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id == from_user_id:
        await message.reply_text("» YOU CAN'T GBAN YOURSELF!")
    elif user_id == BOT_ID:
        await message.reply_text("» YOU CAN'T GBAN MYSELF NOOB!")
    elif user.id in SUDO_USERS:
        await message.reply_text("» Abe Lode Tu thoda sa bhen ka loda hai kya 🤣🤣!")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("**User Already In Gban List.**")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**GLOBALLY BANNING {mention}**\n\nEXPECTED TIME : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
**GLOBALLY BAN ON {BOT_NAME}**
**• CHAT :** {message.chat.title} [`{message.chat.id}`]
**• SUDOER :** {from_user_mention}
**• USER :** {mention}
**• USER ID :** `{user_id}`
**• BANNED IN :** {number_of_chats} chats"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDO_USERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**EXAMPLE :**\n/ungban [USERNAME|USER ID]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user_id == from_user_id:
            await message.reply_text("» You Can't Gban yourself!")
        elif user_id == BOT_ID:
            await message.reply_text("» I Can't Gban Myself") 
        elif user_id in SUDO_USERS:
            await message.reply_text("» I Can't Gban Sudo User!")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("» This User is not gbanned!")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"» Removed from gbanlist")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id == from_user_id:
        await message.reply_text("» You Can't Gban yourself!")
    elif user_id == BOT_ID:
        await message.reply_text(
            "» I Can't Gban Myself"
        ) 
    elif user_id in SUDO_USERS:
        await message.reply_text("» I Can't Gban Sudo User!")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("» This user is not gbanned!")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"» USER REMOVED FROM GBAN LIST...")



chat_watcher_group = 5

@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.kick_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"{checking} IS GLOBALLY BANNED ON {BOT_NAME}"
        )
