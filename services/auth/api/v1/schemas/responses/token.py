from typing import Optional

from pydantic import BaseModel, Field


class ResponseTokenInfo(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"


class ResponseTokenInfoWithoutRefresh(ResponseTokenInfo):
    refresh_token: Optional[str] = Field(exclude=True, default=None)
