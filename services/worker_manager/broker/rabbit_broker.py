from faststream.rabbit import RabbitBroker
from core.config import SETTINGS
from broker.subs import worker_router

broker = RabbitBroker(
    url=SETTINGS.rabbit_mq.get_amqp_url(),
)

broker.include_router(worker_router)
