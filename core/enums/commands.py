from enum import StrEnum


class CliCommand(StrEnum):
    SET_INTERVAL = "interval"
    START_FLOOD = "start"
    STOP_FLOOD = "stop"

    HELP = "help"
    CLIENT_INFO = "info"
    PARSE_CHATS = "parse"
