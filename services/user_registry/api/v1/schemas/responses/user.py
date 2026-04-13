from tortoise.contrib.pydantic import pydantic_model_creator
from infrastructure.database.models import UserModel

UserResponseModel = pydantic_model_creator(
    UserModel,
    name="UserResponse",
    exclude=()
)
