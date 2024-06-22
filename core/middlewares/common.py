from multiprocessing.connection import Client
from typing import Any

from pyrogram_patch.middlewares.middleware_types import OnUpdateMiddleware
from pyrogram_patch.patch_helper import PatchHelper

from core.app_config import AppConfig
from utils.json_manager import JSONManager


class CommonMiddleware(OnUpdateMiddleware):
    """
    This class is a middleware that is used to provide common functionality to the bot.

    Args:
        config (AppConfig): The application configuration.
        json_manager (JSONManager): A JSON manager that can be used to read and write JSON files.
    """

    def __init__(self, config: AppConfig, json_manager: JSONManager):
        self.config = config
        self.json_manager = json_manager

    async def __call__(self, update: Any, client: Client, patch: PatchHelper):
        patch.data["json_manager"] = self.json_manager
        patch.data["config"] = self.config
