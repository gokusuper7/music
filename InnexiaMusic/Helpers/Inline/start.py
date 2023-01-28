
import config

from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)
from InnexiaMusic import BOT_USERNAME, OWNER_ID


def start_pannel():
        buttons = [
            [
                InlineKeyboardButton(
                    text="➕ Add Me Else Gey ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🥀 Owner 🥀", user_id=OWNER_ID
                ),
                InlineKeyboardButton(
                    text="Help 📕", callback_data="help_start"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Support", url=config.SUPPORT_CHAT
                ),
                InlineKeyboardButton(
                    text="Channel 💘", url=config.SUPPORT_CHANNEL
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Source Code 🌐", url="https://github.com/Team-Deadly/Music"
                ),
            ],
        ]
        return buttons


def private_panel():
        buttons = [
            [
                InlineKeyboardButton(
                    text="➕ Add Me Else Gey ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🥀 Owner 🥀", user_id=OWNER_ID
                ),
                InlineKeyboardButton(
                    text="Help 📕", callback_data="help_start"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Support", url=config.SUPPORT_CHAT
                ),
                InlineKeyboardButton(
                    text="Channel 💘", url=config.SUPPORT_CHANNEL
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Source Code 🌐", url="https://github.com/Team-Deadly/Music"
                ),
            ],
        ]
        return buttons
