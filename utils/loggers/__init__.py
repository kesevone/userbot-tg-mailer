import logging

from .multiline import MultilineLogger

__all__ = ["setup_logger", "MultilineLogger", "client_log", "service", "database"]

client_log: logging.Logger = logging.getLogger("CLIENT")
service: logging.Logger = logging.getLogger("SERVICE")
database: logging.Logger = logging.getLogger("DATABASE")


def setup_logger(level: int = logging.INFO) -> None:
    for name in [
        "pyrogram.connection.connection",
        "pyrogram.session.session",
        "pyrogram.dispatcher",
    ]:
        logging.getLogger(name).propagate = False

    logging.basicConfig(
        format="[%(asctime)s | %(levelname)s | %(name)s] — %(message)s",
        datefmt="%H:%M:%S",
        level=level,
    )
