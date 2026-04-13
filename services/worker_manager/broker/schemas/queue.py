from typing import Literal
from pydantic import BaseModel, Field

from broker.schemas.base import BaseMessageResponseSchema, CommandTypes


# Minimal payloads for queue
class QueueNamePayloadSchema(BaseModel):
    queue_name: str = Field()


# Used response queue schemas
class QueueResponseCreateMessageSchema(BaseMessageResponseSchema[QueueNamePayloadSchema]):
    command_type: Literal[CommandTypes.queue_create]
