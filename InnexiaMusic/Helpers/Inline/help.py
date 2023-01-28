
from InnexiaMusic import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


help_panel = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ADMINS",
                    callback_data="help_callback ADMIN",
                ),
                InlineKeyboardButton(
                    text="AUTH",
                    callback_data="help_callback AUTH",
                ),
                InlineKeyboardButton(
                    text="PLAY",
                    callback_data="help_callback PLAY",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="OWNER",
                    callback_data="help_callback OWNER",
                ),
                InlineKeyboardButton(
                    text="SUDO",
                    callback_data="help_callback SUDO",
                ),
                InlineKeyboardButton(
                    text="TOOLS",
                    callback_data="help_callback TOOLS",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="◀️Back",
                    callback_data=f"home",
                ),
                InlineKeyboardButton(
                    text="Close🗑",
                    callback_data=f"close"
                ),
            ]
        ]
    )


help_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="◀️Back",
                    callback_data=f"home",
                ),
                InlineKeyboardButton(
                    text="Close🗑",
                    callback_data=f"close"
                ),
            ]
        ]
    )
