import os
import re
import config
import asyncio
import importlib

from rich.table import Table
from rich.console import Console as hehe
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch

from InnexiaMusic.Helpers.Logging import *
from InnexiaMusic.Helpers.PyTgCalls.AsuX import run
from InnexiaMusic.Modules import ALL_MODULES
from InnexiaMusic.Helpers.Inline import private_panel
from InnexiaMusic.Helpers.Database import get_active_chats, remove_active_chat, add_served_user
from InnexiaMusic import (ASSID, ASSMENTION, ASSNAME, ASSUSERNAME, BOT_ID, BOT_NAME, BOT_USERNAME, SUDO_USERS, F_OWNER, db, app, Ass)

loop = asyncio.get_event_loop()
console = hehe()
HELPABLE = {}


async def InnexiaBot():
    with console.status(
        "[magenta] Booting InnexiaMusic...",
    ) as status:
        console.print("┌ [red]Clearing mongodb cache...")
        try:
            chats = await get_active_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_chat(chat_id)
        except Exception as e:
            console.print("[red] Error in clearing mongodb cache.")
        console.print("└ [green]mongodb cleared successfully!\n\n")
        ____ = await startup_msg("**» Importing Modules...**")
        status.update(
            status="[bold blue]Scanning Plugins...", spinner="earth"
        )
        await asyncio.sleep(0.7)
        console.print("Found {} Plugins".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Importing Plugins...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        await asyncio.sleep(1.2)
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "InnexiaMusic.Modules." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f"✨ [bold cyan]Successfully Imported: [green]{all_module}.py"
            )
            await asyncio.sleep(0.1)
        console.print("")
        _____ = await startup_edit(____, f"**» Successfully Imported {(len(ALL_MODULES))} modules...**")
        status.update(
            status="[bold blue]All modules imported successfully!",
        )
        await asyncio.sleep(0.2)
        SUDO_USERS.append(int(BOTINFOID))
        await startup_del(_____)
    console.print(
        "[bold green]Trying to start the bot...\n"
    )
    try:
        await app.send_message(
            config.LOGGER_ID,
            f"<b>➻ MusicBot Successfully Started🔮 As {ASSNAME} </b>",
        )
    except Exception as e:
        print(
            "Bot has failed to access the log group. Make sure that you have added your Bot to your log group and promoted as Admin!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    a = await app.get_chat_member(config.LOGGER_ID, BOT_ID)
    if a.status != "administrator":
        print("Promote bot as admin in logger group")
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await Ass.send_message(
            config.LOGGER_ID,
            f"<b>➻ MusicBot Assistant Started Successfully as {ASSNAME} <b>",
        )
    except Exception as e:
        print(
            "Assistant Account failed to access the log group. Make sure that you have added the assistant to your log group and promoted as admin!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await Ass.join_chat("TheDeadlyBots")
        await Ass.join_chat("TheBotUpdates")
    except:
        pass
    console.print(f"\n┌[red] Bot Started As {BOT_NAME}!")
    console.print(f"├[green] Assistant Startes As {ASSNAME}!")
    await run()
    console.print(f"\n[red]Stopping Bot") 

if __name__ == "__main__":
    loop.run_until_complete(AsuX_boot())
