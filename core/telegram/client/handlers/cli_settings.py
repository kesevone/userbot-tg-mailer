from typing import Any

from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram_patch.router import Router

from core.enums.commands import CliCommand
from core.services.database.models.general import ClientModel
from core.services.database.gateways.general import Gateway
from utils.loggers import database

router = Router()


@router.on_message(
    filters.private & filters.me & filters.command(CliCommand.SET_INTERVAL, prefixes="")
)
async def on_set_interval(_: Client, msg: Message, gateway: Gateway):
    interval: str = msg.text.replace(CliCommand.SET_INTERVAL, "").strip()

    if not interval or not interval.isdigit():
        return await msg.reply(
            "➡️ Enter the <b>interval</b> of sending the message in seconds, for example <code>interval 15</code>."
        )

    interval: int = int(interval)
    user_id: int = msg.from_user.id
    db_cli: ClientModel = await gateway.client.get(user_id=user_id)

    copy_settings: dict[str, Any] = db_cli.settings.copy()
    copy_settings["seconds_interval"] = interval

    db_cli.update_settings(settings=copy_settings)
    await gateway.commit(db_cli)

    database.info(
        "Settings updated. Client ID: (%d) | Seconds interval: (%d)", user_id, interval
    )

    return await msg.reply(
        "🕖 <b>Interval</b> for sending a message in <code>{seconds_interval} seconds</code> has been successfully set!".format(
            seconds_interval=interval
        )
    )
