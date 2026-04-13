from uuid import UUID

from pydantic import EmailStr, BaseModel


class UserRegisteredSchema(BaseModel):
    auth_id: UUID
    email: EmailStr

class EmailUpdateSchema(BaseModel):
    auth_id: UUID
    old_email: EmailStr
    new_email: EmailStr
