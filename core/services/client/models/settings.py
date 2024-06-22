from pydantic import BaseModel


class SettingsModel(BaseModel):
    seconds_interval: int = 5