from ..redis_client import RedisClient, get_basic_redis_client
from .task_repository import TaskRepository


class RepositoryFactory:
    @staticmethod
    def get_task_repository(redis_client: RedisClient) -> TaskRepository:
        return TaskRepository(redis_client)


base_radis_client = get_basic_redis_client()
task_repo = RepositoryFactory.get_task_repository(base_radis_client)

__all__ = (
    "task_repo",
)
