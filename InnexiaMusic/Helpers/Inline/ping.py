import config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ping_ig = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Close🗑",
                    callback_data="close",
                ),                
            ]
        ]
    )
