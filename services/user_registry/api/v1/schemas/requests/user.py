from pydantic import Field, BaseModel, EmailStr


class RequestCreateUserModel(BaseModel):
    username: str = Field(max_length=32)
    email: EmailStr = Field()
