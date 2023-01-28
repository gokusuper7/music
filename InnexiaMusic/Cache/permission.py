
from typing import Dict, List, Union

from InnexiaMusic import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "» PLEASE GIVE ME BELOW PERMISSION:\n\n"
                + "\n• **DELETE MESSAGES**"
                + "\n• **MANAGE VOICE CHATS**"
                + "\n• **INVITE USERS VIA LINK.**"
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "» I DON'T HAVE PERMISSION TO:"
                + "\n\n**MANAGE VOICE CHAT.**"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "» I DON'T HAVE PERMISSION TO:"
                + "\n\n**DELETE MESSAGES.**"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "» I DON'T HAVE PERMISSION TO:"
                + "\n\n**INVITE USERS VIA LINK.**"
            )
            return
        return await mystic(_, message)

    return wrapper
