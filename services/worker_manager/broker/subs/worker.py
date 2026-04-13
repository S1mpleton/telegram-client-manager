from faststream.rabbit import RabbitRouter

from broker.schemas import (
    ResponseWorkerMessage,
)
from core.command_operations import command_route
from core.config import MQ_WORKERS_QUEUE

router = RabbitRouter()


@router.subscriber(MQ_WORKERS_QUEUE)
async def workers_handler(data: ResponseWorkerMessage) -> None:


    executor = command_route.get(data.command_type)

    await executor(data)
