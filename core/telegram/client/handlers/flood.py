import asyncio
import time
from asyncio import Task
from typing import Any, List

from pyrogram import filters, Client
from pyrogram.errors import BadRequest, ChatForbidden, NotAcceptable
from pyrogram.types import Message
from pyrogram_patch.router import Router

from core.app_config import AppConfig
from core.enums.commands import CliCommand
from core.services.database.context import SQLSessionContext
from core.services.database.create_pool import create_pool
from core.services.database.models.general import ChatModel, ClientModel, FloodHistoryModel
from utils.jinja_formatter import Jinja
from utils.loggers import client_log, service

router = Router()


@router.on_message(
    filters.private & filters.me & filters.command(CliCommand.START_FLOOD, prefixes="")
)
async def on_start_flood(cli: Client, msg: Message, config: AppConfig):
    user_id: int = msg.from_user.id
    text: str = msg.text.html.replace(CliCommand.START_FLOOD, "")

    if not text:
        return await msg.reply(
            "➡️ Enter your mailing text in any format (HTML formatting supported):"
        )

    _: Task = asyncio.create_task(
        start_flood(cli=cli, config=config, user_id=user_id, text=text)
    )

    return await msg.reply("🔘 <b>Mailing started</b>!")


@router.on_message(
    filters.private & filters.me & filters.command(CliCommand.STOP_FLOOD, prefixes="")
)
async def on_stop_flood(_: Client):
    raise NotImplementedError()


async def start_flood(cli: Client, config: AppConfig, user_id: int, text: str):
    _, session = create_pool(
        dsn=config.sqlite.build_dsn(), enable_logging=config.sqlite.enable_logging
    )
    async with SQLSessionContext(session_pool=session) as gw:
        db_cli: ClientModel = await gw.client.get(user_id=user_id)
        settings: dict[str, Any] = db_cli.settings
        seconds_interval: int = settings.get("seconds_interval", 5)

        flood_history: FloodHistoryModel = FloodHistoryModel.create(
            user_id=user_id, settings=settings, text=text
        )

        cli_chats: List[ChatModel] = await gw.chat.get_all(user_id=user_id)
        if not cli_chats:
            service.info("Chats for mailing were not found, stopping mailing..")
            text: str = await Jinja(
                "❌ <b>No chats found</b> for mailing, use <code>{{ command }}</code> to start parsing.\n"
                "Also, make sure you <b>set the message interval</b>!",
                command=CliCommand.PARSE_CHATS,
            ).render()
            return await cli.send_message(chat_id="self", text=text)

        good_chats = 0
        bad_chats = 0
        service.info("Mailing started. Total chats: (%d) | Interval: (%d)", len(cli_chats), seconds_interval)

        start_time = int(time.time())
        for chat in cli_chats:
            try:
                await cli.send_message(chat_id=int(chat.id), text=text)
                service.info(
                    "Message sent. Chat ID: (%d) | Chat name: (%s) | Client ID: (%d)",
                    chat.id,
                    chat.name,
                    chat.user_id,
                )
                good_chats += 1
                await asyncio.sleep(seconds_interval)
            except (BadRequest, NotAcceptable, ChatForbidden) as e:
                bad_chats += 1
                db_chat: ChatModel = await gw.chat.get(chat_id=chat.id)
                await gw.delete(db_chat)
                client_log.warning(
                    "Failed to send message, Chat ID (%d). The chat has been removed from the database. Error: {%s}",
                    chat.id,
                    e
                )
        end_time = int(time.time())

        if good_chats:
            flood_history.update_status(status=True)
        else:
            flood_history.update_status(status=False)

        await gw.commit(flood_history)

        service.info(
            "Mailing is complete. Good chats: (%d) | Bad chats: (%d)\n",
            good_chats,
            bad_chats,
        )

        text: str = await Jinja(
            "✅ <b>Mailing completed successfully.</b>\n\n"
            "<b>Success chats:</b> <code>{{ good_chats }}</code>\n"
            "<b>Error chats:</b> <code>{{ bad_chats }}</code>\n\n"
            "<b>Total time for mailing:</b> <code>{{ total_time }}s</code>\n"
            "{% if bad_chats %}"
            "⚠️ Chats where messages <b>could not be sent</b> have been deleted. <b>Parse the chats again</b>, or check them manually."
            "{% endif %}",
            good_chats=good_chats,
            bad_chats=bad_chats,
            total_time=(end_time - start_time),
        ).render()
        return await cli.send_message(chat_id="self", text=text)
