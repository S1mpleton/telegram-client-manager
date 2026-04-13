import asyncio

from typing import TYPE_CHECKING, cast
import logging
from aio_pika.message import IncomingMessage, Message
from pydantic import BaseModel

from core.schemas import (
    QueueSchema,
    QueueStatuses,
    ResponseQueueSchema,
    ResponseObjectSeverities,
    ResponseObjectTypes
)
from rabbit import RabbitBase

import config

if TYPE_CHECKING:
    from aio_pika.abc import AbstractRobustQueue


class Worker(RabbitBase):
    def __init__(
            self,
            input_queue_name: str = config.MQ_INPUT_QUEUE,
            output_queue_name: str = config.MQ_OUTPUT_QUEUE,
            host: str = config.RMQ_HOST,
            port: int = config.RMQ_PORT,
            login: str = config.RMQ_USER,
            password: str = config.RMQ_PASSWORD,
    ):
        super().__init__(host, port, login, password)

        self.input_queue_name: str = input_queue_name
        self.output_queue_name: str = output_queue_name

        self.input_queue: AbstractRobustQueue | None = None
        self.output_queue: AbstractRobustQueue | None = None

    async def setup_queues(self):
        self.input_queue = await self.queue_declare(
            self.input_queue_name,
            exclusive=True,
        )

        self.output_queue = await self.queue_declare(
            self.output_queue_name,
            durable=True
        )

    @staticmethod
    def parse_message_from_pydantic(model: BaseModel):
        return Message(
            content_type="application/json",
            content_encoding="utf-8",
            body=model.model_dump_json().encode("utf-8")
        )

    async def send_message(self, message: Message):
        if not self._channel:
            raise RuntimeError("Channel not initialized")

        await self._channel.default_exchange.publish(
            message,
            routing_key=self.output_queue_name
        )

    @staticmethod
    async def process_message(message: IncomingMessage):
        try:
            body = message.body.decode()

            await message.ack()

        except Exception as e:
            await message.reject(requeue=False)
            print(f"Error processing message: {e}")
            logging.info(f"Error processing message: {e}")

    async def start(self):
        notification_strt_message = self.parse_message_from_pydantic(
            ResponseQueueSchema(
                severity=ResponseObjectSeverities.info,
                object=ResponseObjectTypes.queue,
                detail="Unique worker's queue was created",
                data=QueueSchema(
                    name=self.input_queue_name,
                    status=QueueStatuses.ready
                )
            )
        )
        await self.connect()
        await self.setup_queues()

        await self.send_message(notification_strt_message)

        async with self.input_queue.iterator() as queue_iter:
            async for message in queue_iter:
                await self.process_message(cast(IncomingMessage, message))

        print("STARTDE")
        logging.info("Worker started")

    async def stop(self):
        await self.disconnect()
        logging.info("Worker stopped")


async def main():
    worker = Worker()
    try:
        await worker.start()
        print("Test")
    except KeyboardInterrupt:
        await worker.stop()
    except Exception as e:
        print(f" [!!] Error: {e}")
        await worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
