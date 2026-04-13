from typing import TYPE_CHECKING, Optional
import aio_pika

import config
from rabbit.exception import RabbitException

if TYPE_CHECKING:
    from aio_pika.abc import AbstractRobustQueue


class RabbitBase:
    def __init__(
            self,
            host: str = config.RMQ_HOST,
            port: int = config.RMQ_PORT,
            login: str = config.RMQ_USER,
            password: str = config.RMQ_PASSWORD,
    ):
        self.host = host
        self.port = port
        self.login = login
        self.password = password

        self._connection: Optional[aio_pika.RobustConnection] = None
        self._channel: Optional[aio_pika.RobustChannel] = None

    @property
    def channel(self) -> aio_pika.RobustChannel:
        if self._channel is None:
            raise RabbitException("Use context manager for Rabbit helper")

        return self._channel

    async def queue_declare(
            self,
            queue_name: str,
            exclusive: bool = False,
            auto_delete: bool = False,
            durable: bool = False
    ) -> "AbstractRobustQueue":
        return await self._channel.declare_queue(
            queue_name,
            exclusive=exclusive,
            auto_delete=auto_delete,
            durable=durable,
        )

    async def connect(
            self,
            prefetch_count: int = 1
    ):
        if not self._connection or self._connection.is_closed:
            self._connection = await aio_pika.connect_robust(
                host=self.host,
                port=self.port,
                login=self.login,
                password=self.password
            )
            self._channel = await self._connection.channel()
            await self._channel.set_qos(prefetch_count=prefetch_count)

    async def disconnect(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()

        if self._connection and not self._connection.is_closed:
            await self._connection.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
