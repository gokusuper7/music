import config
from InnexiaMusic import BOT_USERNAME, app
from InnexiaMusic.Helpers.Database import is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "**» YOU'RE AN ANONYMOUS ADMIN\n\n• revert back to original account to use me.**"
            )
        if await is_on_off(1):
            if int(message.chat.id) != int(LOGGER_ID):
                return await message.reply_text(
                    f"» {BOT_NAME} IS UNDER MAINTENANCE.", 
                    disable_web_page_preview=True,
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"**» GLOBALLY BANNED USER «**\n\nACCOURDING  TO MY DATABASE YOU'RE GBANNED BY OWNER, SO YOU CAN'T USE ME.\n\nVISIT : [SUPPORT GROUP]({config.SUPPORT_CHAT})",
                 disable_web_page_preview=True,
            )
        return await mystic(_, message)

    return wrapper


def checkerCB(mystic):
    async def wrapper(_, CallbackQuery):
        if await is_on_off(1):
            if int(CallbackQuery.message.chat.id) != int(LOGGER_ID):
                return await CallbackQuery.answer(
                    "» {BOT_NAME} IS UNDER MAINTENANCE.",
                    show_alert=True,
                )
        if await is_gbanned_user(CallbackQuery.from_user.id):
            return await CallbackQuery.answer(
                "**» GBANNED USER CLICK**\n\nYou cannot perform this action cause you are an gbanned user", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
