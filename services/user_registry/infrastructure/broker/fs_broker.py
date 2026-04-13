from faststream.rabbit import RabbitBroker
from core.config import SETTINGS
from infrastructure.broker.subs.users import router as users_router

broker = RabbitBroker(
    url=SETTINGS.faststream.get_amqp_url(),
)

broker.include_router(users_router)