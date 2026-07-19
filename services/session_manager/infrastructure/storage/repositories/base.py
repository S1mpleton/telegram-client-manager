from typing import TYPE_CHECKING
from abc import ABC

from infrastructure.storage.redis_client import RedisClient

if TYPE_CHECKING:
    from redis.asyncio.client import Redis


class BaseRepository(ABC):
    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    @property
    def redis(self) -> "Redis":
        return self.redis_client.redis
