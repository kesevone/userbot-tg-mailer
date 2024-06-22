from typing import Self

from pydantic import SecretStr, BaseModel
from pydantic_settings import BaseSettings as _BaseSettings, SettingsConfigDict


class BaseSettings(_BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


class SQLiteConfig(BaseSettings, env_prefix="SQLITE_"):
    path: str
    name: str
    enable_logging: bool

    def build_dsn(self) -> str:
        return "sqlite+aiosqlite:///{path}/{name}.db".format(
            path=self.path, name=self.name
        )


class ClientConfig(BaseSettings, env_prefix="CLIENT_"):
    api_id: SecretStr
    api_hash: SecretStr
    session_name: str
    session_path: str


class AppConfig(BaseModel):
    client: ClientConfig
    sqlite: SQLiteConfig

    @classmethod
    def create(cls) -> Self:
        return cls(
            client=ClientConfig(),
            sqlite=SQLiteConfig(),
        )