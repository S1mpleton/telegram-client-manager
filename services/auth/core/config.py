from pydantic import BaseModel, Field, ConfigDict
from pathlib import Path

from pydantic_settings import BaseSettings
import asyncio

# from core.generate_certs import GeneratorCerts

BASE_URL = "127.0.0.1:8001"

BASE_PATH = Path(__file__).parent.parent
DATABASE_PATH = BASE_PATH.joinpath("infrastructure").joinpath("database")
CERTS_DIR = BASE_PATH.joinpath("certs")


# GeneratorCerts(CERTS_DIR)

class EmailConfig(BaseModel):
    SMTP_HOST: str = "smtp.mail.ru"
    SMTP_PORT: int = 465
    SMTP_USERNAME: str = "stepfatherbot@internet.ru"
    SMTP_FROM_EMAIL: str = "stepfatherbot@internet.ru"
    SMTP_PASSWORD: str = "gpzfqIDcMOElHwmrtglp"


class RedisConfig(BaseModel):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=6300)
    password: str = Field(default="guest")
    db: int = Field(default=0)


class AuthJWT(BaseModel):
    private_key_path: Path = CERTS_DIR.joinpath("jwt-private-key.pem")
    public_key_path: Path = CERTS_DIR.joinpath("jwt-public-key.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 3


class FastStreamConfig(BaseModel):
    message_type: str = Field(default="application/json")
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=5600)
    login: str = Field(default="guest")
    password: str = Field(default="guest")

    def get_amqp_url(self):
        return f"amqp://{self.login}:{self.password}@{self.host}:{self.port}/"


class DatabaseConfig(BaseModel):
    path_to_config: Path = Field(default=DATABASE_PATH.joinpath("database_config.json"))
    timezone: str = Field(default="Europe/Moscow")


class Settings(BaseModel):
    auth_jwt: AuthJWT = Field(default_factory=AuthJWT)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    faststream: FastStreamConfig = Field(default_factory=FastStreamConfig)
    email: EmailConfig = Field(default_factory=EmailConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)



SETTINGS = Settings()

