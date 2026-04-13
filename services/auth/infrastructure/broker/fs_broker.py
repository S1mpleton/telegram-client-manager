from faststream.rabbit import RabbitBroker
from core.config import SETTINGS

broker = RabbitBroker(
    url=SETTINGS.faststream.get_amqp_url(),
)

user_registered = broker.publisher(
    "user-registered"
)

email_update = broker.publisher(
    "email-update"
)

