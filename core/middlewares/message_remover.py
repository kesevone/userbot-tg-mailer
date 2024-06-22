from multiprocessing.connection import Client

from pyrogram.types import Message
from pyrogram_patch.middlewares.middleware_types import OnMessageMiddleware
from pyrogram_patch.patch_helper import PatchHelper

from core.enums.commands import CliCommand


class MessageRemoverMiddleware(OnMessageMiddleware):

    async def __call__(self, msg: Message, client: Client, patch: PatchHelper):
        command = msg.command.copy().pop(0)
        if command in [command.lower() for command in CliCommand]:
            return await msg.delete()
