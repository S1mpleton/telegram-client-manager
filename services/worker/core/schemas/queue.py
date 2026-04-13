from enum import StrEnum

from pydantic import BaseModel, Field

from core.schemas.schemas import BaseResponseSchema


class QueueStatuses(StrEnum):
    ready = "READY"
    invalid = "INVALID"


class QueueSchema(BaseModel):
    name: str = Field()
    status: QueueStatuses = Field(default=QueueStatuses.ready)


class ResponseQueueSchema(BaseResponseSchema):
    data: QueueSchema
