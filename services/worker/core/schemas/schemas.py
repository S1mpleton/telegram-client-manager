from enum import StrEnum

from pydantic import BaseModel, Field


class ResponseObjectTypes(StrEnum):
    worker = "WORKER"
    queue = "QUEUE"
    client = "CLIENT"

class ResponseObjectSeverities(StrEnum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"


class BaseResponseSchema(BaseModel):
    severity: ResponseObjectSeverities = Field()
    object: ResponseObjectTypes = Field()
    detail: str = Field()


