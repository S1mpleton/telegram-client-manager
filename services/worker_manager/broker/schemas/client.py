from typing import Literal, Union

from pydantic import BaseModel, Field

from api.v1.schemas import ClientAuthSchema, BotAuthSchema
from broker.schemas.base import (
    BaseMessageSchema,
    CommandTypes,
    BaseMessageResponseSchema
)


# Minimal payloads for client
class UserIDPayloadSchema(BaseModel):
    user_id: int = Field()


class CIDPayloadSchema(BaseModel):
    cid: int = Field()


class SessionStringPayloadSchema(BaseModel):
    session_string: str = Field()


class ClientNamePayloadSchema(BaseModel):
    client_name: str = Field(max_length=16)


# Payloads for client
class BotAuthPayloadSchema(BotAuthSchema, UserIDPayloadSchema):
    pass


class ClientAuthPayloadSchema(ClientAuthSchema, UserIDPayloadSchema):
    pass


class ClientStartPayloadSchema(SessionStringPayloadSchema, ClientNamePayloadSchema, UserIDPayloadSchema):
    pass


class ClientStopPayloadSchema(ClientNamePayloadSchema, UserIDPayloadSchema):
    pass


# Used request client's schemas
class BotAuthMessageSchema(BaseMessageSchema[BotAuthPayloadSchema]):
    command_type: Literal[CommandTypes.auth_bot] = CommandTypes.auth_bot


class ClientAuthMessageSchema(BaseMessageSchema[ClientAuthPayloadSchema]):
    command_type: Literal[CommandTypes.auth_client] = CommandTypes.auth_client


class ClientStartMessageSchema(BaseMessageSchema[ClientStartPayloadSchema]):
    command_type: Literal[CommandTypes.client_start] = CommandTypes.client_start


class ClientStopMessageSchema(BaseMessageSchema[ClientStopPayloadSchema]):
    command_type: Literal[CommandTypes.client_stop] = CommandTypes.client_stop


# Payloads for client's responses
class ClientResponseAuthPayloadSchema(SessionStringPayloadSchema, CIDPayloadSchema, UserIDPayloadSchema):
    pass


# Used response client's schemas
class ClientResponseAuthMessageSchema(BaseMessageResponseSchema[ClientResponseAuthPayloadSchema]):
    command_type: Literal[CommandTypes.auth_client, CommandTypes.auth_bot]


class ClientResponseStartMessageSchema(BaseMessageResponseSchema[Union[ClientNamePayloadSchema, UserIDPayloadSchema]]):
    command_type: Literal[CommandTypes.client_start]


class ClientResponseStopMessageSchema(BaseMessageResponseSchema[Union[ClientNamePayloadSchema, UserIDPayloadSchema]]):
    command_type: Literal[CommandTypes.client_stop]
