from faststream.rabbit import RabbitRouter

from infrastructure.broker.schemas.user import UserRegisteredSchema, EmailUpdateSchema
from infrastructure.database import CRUD, UserCreateSchema, UserUpdateSchema

router = RabbitRouter()


@router.subscriber("user-registered")
async def register(user_registered: UserRegisteredSchema) -> None:
    await CRUD.create_user(UserCreateSchema(**user_registered.model_dump()))
    print("user_registered ", user_registered)


@router.subscriber("email-update")
async def update_email(email_update_schema: EmailUpdateSchema) -> None:
    await CRUD.update_user_by_email(
        email_update_schema.old_email,
        UserUpdateSchema(email=email_update_schema.new_email)
    )
    print("email_update ", email_update_schema)