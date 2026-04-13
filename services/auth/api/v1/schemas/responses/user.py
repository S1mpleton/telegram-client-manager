from pydantic import Field

from infrastructure.database.schemas import (
    UserOutSchema,
    TortoiseUserOutSchema,
    UserModel
)


class ResponseUserSchema(UserOutSchema):
    id: int = Field(exclude=True)

    @classmethod
    async def from_tortoise(cls, auth_model: UserModel):
        user_data = await TortoiseUserOutSchema.from_tortoise_orm(auth_model)
        return cls(
            **user_data.model_dump(exclude={'id'})
        )
