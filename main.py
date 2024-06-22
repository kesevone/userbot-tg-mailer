from pyrogram import Client

from core.app_config import AppConfig
from core.factory.client import create_client
from utils.json_manager import JSONManager
from utils.loggers import setup_logger


setup_logger()
config: AppConfig = AppConfig.create()
json_manager: JSONManager = JSONManager()
client: Client = create_client(config=config, json_manager=json_manager)

if __name__ == "__main__":
    client.run()
