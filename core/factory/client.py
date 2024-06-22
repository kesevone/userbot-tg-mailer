from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram_patch import patch, PatchManager

from core.app_config import AppConfig
from core.middlewares.client import ClientMiddleware
from core.middlewares.common import CommonMiddleware
from core.middlewares.database import DBSessionMiddleware
from core.middlewares.message_remover import MessageRemoverMiddleware
from core.services.database.create_pool import create_pool
from core.telegram.client.handlers import cli_settings, common, flood
from utils.json_manager import JSONManager
from utils.loggers import client_log


def setup_middlewares(
    patch_manager: PatchManager, config: AppConfig, json_manager: JSONManager
) -> None:

    engine, session = create_pool(
        dsn=config.sqlite.build_dsn(), enable_logging=config.sqlite.enable_logging
    )

    for middleware in [
        DBSessionMiddleware(engine=engine, session_pool=session),
        CommonMiddleware(config=config, json_manager=json_manager),
        ClientMiddleware(),
        MessageRemoverMiddleware(),
    ]:
        patch_manager.include_middleware(middleware)


def setup_routers(patch_manager: PatchManager) -> None:
    for router in [cli_settings.router, common.router, flood.router]:
        patch_manager.include_router(router)


def create_client(config: AppConfig, json_manager: JSONManager) -> Client:

    client = Client(
        name=config.client.session_name,
        api_id=config.client.api_id.get_secret_value(),
        api_hash=config.client.api_hash.get_secret_value(),
        workdir=config.client.session_path,
        parse_mode=ParseMode.HTML,
    )
    patch_manager = patch(client)

    setup_middlewares(patch_manager, config, json_manager)
    setup_routers(patch_manager)

    client_log.info(
        "Client-app successfully patched. Middlewares and routers installed."
    )
    return client
