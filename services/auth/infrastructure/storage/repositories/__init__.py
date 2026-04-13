from ..redis_client import RedisClient, get_basic_redis_client
from .task_repository import PayloadRepository


class RepositoryFactory:
    @staticmethod
    def get_task_repository(redis_client: RedisClient) -> PayloadRepository:
        return PayloadRepository(redis_client)


base_radis_client = get_basic_redis_client()
pyload_repository = RepositoryFactory.get_task_repository(base_radis_client)

__all__ = (
    "pyload_repository",
)
