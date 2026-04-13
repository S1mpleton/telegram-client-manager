from pydantic import BaseModel, Field
from typing import Optional


class BaseAuthSchema(BaseModel):
    name: str = Field(max_length=16)
    api_id: str = Field()
    api_hash: str = Field(max_length=32)


class BotAuthSchema(BaseAuthSchema):
    bot_token: str = Field(max_length=46)


class ClientAuthSchema(BaseAuthSchema):
    phone_number: Optional[str] = Field()

