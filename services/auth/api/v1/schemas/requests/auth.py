from pydantic import BaseModel, EmailStr, Field


class RequestAuthSchema(BaseModel):
    email: EmailStr = Field(description="Auth email")
    password: str = Field(description="Auth password", max_length=32)

class RequestVerifyEmailSchema(BaseModel):
    verification_code: str = Field(description="Confirmation code", max_length=8)

class RequestUpdateEmailSchema(BaseModel):
    email: EmailStr = Field(description="New email")
