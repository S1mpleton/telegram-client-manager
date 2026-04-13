from typing import Optional, TYPE_CHECKING
from redis.exceptions import ConnectionError, TimeoutError
import redis.asyncio as redis

from core.config import SETTINGS

if TYPE_CHECKING:
    from redis.asyncio.client import Redis


class RedisClient:
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6379,
            db: int = 0,
            password: Optional[str] = None,
            ssl: bool = False,
            max_connections: int = 10,
            timeout: float = 5.0,
            retry_on_timeout: bool = True,
            decode_responses: bool = True,
            **kwargs
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.ssl = ssl
        self.max_connections = max_connections
        self.timeout = timeout
        self.retry_on_timeout = retry_on_timeout
        self.decode_responses = decode_responses
        self.extra_kwargs = kwargs

        self._redis: Optional["Redis"] = None
        self._connection_pool = None

    async def __aenter__(self):
        if not self._redis:
            await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    def _get_redis_url(self) -> str:
        scheme = "rediss" if self.ssl else "redis"
        auth_part = f":{self.password}@" if self.password else ""
        return f"{scheme}://{auth_part}{self.host}:{self.port}/{self.db}"

    async def connect(self) -> None:
        if self._redis is None:
            try:
                self._redis = await redis.from_url(
                    self._get_redis_url(),
                    max_connections=self.max_connections,
                    socket_timeout=self.timeout,
                    socket_connect_timeout=self.timeout,
                    retry_on_timeout=self.retry_on_timeout,
                    decode_responses=self.decode_responses,
                    **self.extra_kwargs
                )
                await self._redis.ping()
            except (ConnectionError, TimeoutError) as e:
                raise ConnectionError(f"Failed to connect to Redis: {e}")

    async def disconnect(self) -> None:
        if self._redis:
            await self._redis.close()
            self._redis = None

    @property
    def redis(self) -> "Redis":
        if self._redis is None:
            raise RuntimeError("Not connected. Call connect() first")
        return self._redis


class RedisClientFactory:
    _instances: dict = {}

    @classmethod
    def get_instance(
            cls,
            host: str = "localhost",
            port: int = 6379,
            db: int = 0,
            **kwargs
    ) -> RedisClient:
        key = f"{host}:{port}:{db}"

        if key not in cls._instances:
            cls._instances[key] = RedisClient(
                host=host,
                port=port,
                db=db,
                **kwargs
            )

        return cls._instances[key]

    @classmethod
    async def close_all(cls) -> None:
        for instance in cls._instances.values():
            await instance.disconnect()
        cls._instances.clear()


def get_basic_redis_client() -> RedisClient:
    return RedisClientFactory.get_instance(
        host=SETTINGS.redis.host,
        port=SETTINGS.redis.port,
        db=SETTINGS.redis.db,
        password=SETTINGS.redis.password
    )
