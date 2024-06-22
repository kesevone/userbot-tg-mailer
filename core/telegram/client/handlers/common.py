from typing import Any, List, Optional

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Chat, Message
from pyrogram_patch.router import Router

from core.enums.commands import CliCommand
from core.services.database.models.general import ChatModel, ClientModel, FloodHistoryModel
from core.services.database.gateways.general import Gateway
from utils.jinja_formatter import Jinja

router = Router()


@router.on_message(
    filters.private & filters.me & filters.command(CliCommand.CLIENT_INFO, prefixes="")
)
async def on_cli_info(_: Client, msg: Message, gateway: Gateway):
    user_id: str = msg.text.replace(CliCommand.CLIENT_INFO, "").strip()
    if not user_id:
        user_id: int = msg.from_user.id

    db_cli: Optional[ClientModel] = await gateway.client.get(user_id=user_id)
    if not db_cli:
        return await msg.reply("❌ <b>Client not found</b>!")

    settings: dict[str, Any] = db_cli.settings
    interval: int = settings.get("seconds_interval")
    chats: List[Optional[ChatModel]] = await gateway.chat.get_all(user_id=user_id)
    flood_history: List[Optional[FloodHistoryModel]] = await gateway.flood_history.get_all(
        user_id=user_id
    )

    text: str = await Jinja(
        "ℹ️ <b>Information about this account <code>{{ full_name }}</code> (<code>{{ user_id }}</code>):</b>\n\n"
        "<b>Number of chats:</b> <code>{{ chats_count }}</code>\n"
        "<b>Total mailings made:</b> <code>{{ flood_history_count }}</code>\n\n"
        "<b>Mailing seconds interval:</b> <code>{{ interval }}</code>",
        chats_count=len(chats),
        flood_history_count=len(flood_history),
        interval=interval,
        full_name=db_cli.fullname,
        user_id=user_id,
    ).render()
    return await msg.reply(text)


@router.on_message(
    filters.private & filters.me & filters.command(CliCommand.PARSE_CHATS, prefixes="")
)
async def on_parse_chats(cli: Client, msg: Message, gateway: Gateway):
    user_id: int = msg.from_user.id

    active_chats: List[Optional[Chat]] = [
        Chat(id=dialog.chat.id, title=dialog.chat.title, type=dialog.chat.type)
        async for dialog in cli.get_dialogs()
        if dialog.chat.type == ChatType.GROUP or dialog.chat.type == ChatType.SUPERGROUP
    ]

    cli_chats: List[Optional[int]] = [
        chat.id for chat in await gateway.chat.get_all(user_id=user_id)
    ]

    new_chats: List[Optional[ChatModel]] = []
    for active_chat in active_chats:
        if active_chat.id not in cli_chats:
            new_chats.append(
                ChatModel().create(
                    chat_id=active_chat.id, user_id=user_id, name=active_chat.title
                )
            )

    if new_chats:
        await gateway.commit(*new_chats)

    text: str = await Jinja(
        "{% if new_chats_count %}"
        "✅ <b>Number of new chats:</b> <code>{{ new_chats_count }}</code>"
        "{% else %}"
        "🥱 <b>No new chats.</b>"
        "{% endif %}",
        new_chats_count=len(new_chats),
    ).render()
    return await msg.reply(text)


@router.on_message(
    filters.private & filters.me & filters.command(CliCommand.HELP, prefixes="")
)
async def on_help(_: Client, msg: Message):
    text: str = await Jinja(
        "❗️ <b>Important information</b> ❗️\n"
        "The developer <b>does not support intrusive spam</b> in chats and does not recommend using it <b>for bad purposes</b>.\n"
        "Use the spammer <b>exclusively for good purposes</b>, for example: sending messages to your chats.\n\n"
        "⚙️ <b>Commands</b>\n"
        "<code>{{ cmd_start }}</code> — starts a mailing to <b>all existing chats.</b> Make sure you parse them. After the command, <b>enter your text</b>.\n"
        "<code>{{ cmd_interval }}</code> — sets the <b>message sending interval</b>, at least <b>5 seconds</b> are recommended.\n\n"
        "<code>{{ cmd_help }}</code> — send this text.\n"
        "<code>{{ cmd_info }}</code> — find out <b>account information</b> (how many chats are in the database and how many mailings have been made, etc). "
        "If you need to take information from another account in the database, enter <code>USER_ID</code> after the command or nothing for current account.\n"
        "<code>{{ cmd_parse }}</code> — <b>parse all chats</b> (group/supergroup), "
        "only <b>once at the start</b> of the script, use only if <b>new chats appear.</b>",
        cmd_start=CliCommand.START_FLOOD,
        cmd_interval=CliCommand.SET_INTERVAL,
        cmd_help=CliCommand.HELP,
        cmd_info=CliCommand.CLIENT_INFO,
        cmd_parse=CliCommand.PARSE_CHATS,
    ).render()
    return await msg.reply(text)
