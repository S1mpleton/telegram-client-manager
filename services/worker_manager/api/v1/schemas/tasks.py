import uuid

from pydantic import BaseModel, Field


class TaskIDSchema(BaseModel):
    task_id: uuid.UUID = Field()
