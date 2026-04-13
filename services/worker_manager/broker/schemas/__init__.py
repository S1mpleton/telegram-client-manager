from typing import Annotated, Union

from .base import (
    CommandTypes,
    ResponseCommandStatuses,
    StorgeCommandStatuses
)
from .client import *
from .queue import *


ResponseWorkerMessage = Annotated[
    Union[
        ClientResponseAuthMessageSchema,
        ClientResponseStartMessageSchema,
        ClientResponseStopMessageSchema,
        QueueResponseCreateMessageSchema
    ],
    Field(discriminator="command_type")
]

__all__ = (
    "ResponseWorkerMessage",

    "CommandTypes",
    "ResponseCommandStatuses",
    "StorgeCommandStatuses",

    # --- queue schemas ---
    "QueueResponseCreateMessageSchema",

    # --- client's payloads
    "BotAuthPayloadSchema",
    "ClientAuthPayloadSchema",
    "ClientStartPayloadSchema",
    "ClientStopPayloadSchema",

    "ClientResponseAuthPayloadSchema",

    # --- client schemas ---
    "BotAuthMessageSchema",
    "ClientAuthMessageSchema",
    "ClientStartMessageSchema",
    "ClientStopMessageSchema",

    "ClientResponseAuthMessageSchema",
    "ClientResponseStartMessageSchema",
    "ClientResponseStopMessageSchema",
)
