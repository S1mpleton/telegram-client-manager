import asyncio

from storage.repositories.base import BaseRepository
from storage import get_basic_redis_client


class TaskRepository(BaseRepository):
    async def set_payload(self, task_id: str, task_data: dict) -> None:
        await self.redis.hset(f"task:{task_id}", mapping=task_data)

    async def get_payload(self, task_id: str) -> dict:
        return await self.redis.hgetall(f"task:{task_id}")

    async def delete_payload(self, task_id: str) -> bool:
        return await self.redis.unlink(f"task:{task_id}")


async def main():
    client = get_basic_redis_client()
    await client.connect()

    await TaskRepository(client).set_payload("aa", {"test3": 789789, "re1": 1, "reer": 44})

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
