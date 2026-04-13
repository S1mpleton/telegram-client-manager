import datetime
from typing import TypeVar, Generic
from zoneinfo import ZoneInfo
from enum import StrEnum

import uuid

from pydantic import BaseModel, Field

T = TypeVar("T")


class CommandTypes(StrEnum):
    client_start = "START"
    client_stop = "STOP"
    auth_bot = "AUTH_BOT"
    auth_client = "AUTH_CLIENT"
    queue_create = "QUEUE_CREATE"


class ResponseCommandStatuses(StrEnum):
    ok = "OK"  # It's ok
    warning = "WARNING"  # It's ok, but there are some nuances
    error = "ERROR"  # Failed command


class StorgeCommandStatuses(StrEnum):
    completed = "COMPLETED" # Command completed
    execution = "EXECUTION"  # Command is being executed
    fatal = "FATAL" # Command failed with an error

class BaseMetadataSchema(BaseModel):
    created_at: datetime.datetime = Field(default=datetime.datetime.now(tz=ZoneInfo("Europe/Moscow")))


class BaseMessageSchema(BaseModel, Generic[T]):
    command_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    command_type: CommandTypes = Field()
    metadata: BaseMetadataSchema = Field(default_factory=BaseMetadataSchema)
    payload: T


class BaseMessageResponseSchema(BaseMessageSchema):
    status: ResponseCommandStatuses = Field()
