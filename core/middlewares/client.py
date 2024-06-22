from multiprocessing.connection import Client
from typing import Any, Optional

from pyrogram.types import Message
from pyrogram_patch.middlewares.middleware_types import OnMessageMiddleware
from pyrogram_patch.patch_helper import PatchHelper

from core.services.client.models import SettingsModel
from core.services.database.models.general import ClientModel
from core.services.database.gateways.general import Gateway
from utils.loggers import service


class ClientMiddleware(OnMessageMiddleware):

    async def __call__(self, msg: Message, client: Client, patch: PatchHelper):
        gw: Gateway = patch.data["gateway"]
        user_id: int = msg.from_user.id

        db_cli: Optional[ClientModel] = await gw.client.get(user_id=user_id)
        if db_cli is None:
            cli_template_settings: dict[str, Any] = SettingsModel().model_dump()
            full_name = f"{msg.from_user.first_name} {msg.from_user.last_name}"
            client: ClientModel = ClientModel.create(
                user_id=user_id, settings=cli_template_settings, fullname=full_name
            )
            await gw.commit(client)
            service.info(
                "Client ID: %s was successfully added to the database.", user_id
            )
