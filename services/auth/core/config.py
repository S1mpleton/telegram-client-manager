from typing import List, Dict

from pydantic import BaseModel, Field
from pathlib import Path
from core.generate_certs import GeneratorCerts

BASE_PATH = Path(__file__).parent.parent
DATABASE_PATH = BASE_PATH.joinpath("core").joinpath("database")
CERTS_DIR = BASE_PATH.joinpath("certs")

# GeneratorCerts(CERTS_DIR)


class AuthJWT(BaseModel):
    private_key_path: Path = CERTS_DIR.joinpath("jwt-private-key.pem")
    public_key_path: Path = CERTS_DIR.joinpath("jwt-public-key.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 3

class DatabaseConfig(BaseModel):
    path_to_config: Path = Field(default=DATABASE_PATH.joinpath("database_config.json"))
    timezone: str = Field(default="Europe/Moscow")


class Settings(BaseModel):
    auth_jwt: AuthJWT = AuthJWT()
    database: DatabaseConfig = DatabaseConfig()


SETTINGS = Settings()
