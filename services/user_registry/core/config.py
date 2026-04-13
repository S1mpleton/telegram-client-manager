from pydantic import BaseModel, Field
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
DATABASE_PATH = BASE_PATH.joinpath("infrastructure").joinpath("database")


class DatabaseConfig(BaseModel):
    path_to_config: Path = Field(default=DATABASE_PATH.joinpath("database_config.json"))
    timezone: str = Field(default="Europe/Moscow")


class FastStreamConfig(BaseModel):
    message_type: str = Field(default="application/json")
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=5600)
    login: str = Field(default="guest")
    password: str = Field(default="guest")

    def get_amqp_url(self):
        return f"amqp://{self.login}:{self.password}@{self.host}:{self.port}/"


class Settings(BaseModel):
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    faststream: FastStreamConfig = Field(default_factory=FastStreamConfig)


SETTINGS = Settings()
