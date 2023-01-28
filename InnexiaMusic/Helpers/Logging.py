import config
from .Clients import app, Ass

failure = "MAKE SURE YOUR BOT IS IN YOUR LOG CHANNEL AND PROMOTED AS ADMIN!"


async def startup_msg(_message_):
    try:
        logto = await app.send_message(
            config.LOGGER_ID, f"{_message_}"
        )
        return logto
    except:
        print(failure)
        return


async def startup_edit(_message_id, _message_):
    try:
        logto = await app.edit_message_text(
            config.LOGGER_ID, _message_id.message_id, f"{_message_}"
        )
        return logto
    except:
        logto = await startup_send_new(_message_)
        return logto


async def startup_del(_message_id):
    try:
        await app.delete_messages(config.LOGGER_ID, _message_id.message_id)
        return bool(1)
    except:
        pass
