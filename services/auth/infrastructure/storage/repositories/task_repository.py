import asyncio
from typing import Optional

from infrastructure.storage.repositories.base import BaseRepository
from infrastructure.storage import get_basic_redis_client


class PayloadRepository(BaseRepository):
    async def set_payload(
            self,
            name: str,
            task_data: dict,
            prefix: Optional[str] = None,
            ttl: Optional[int] = None  # minutes
    ) -> None:
        key = self._get_name(name, prefix)
        await self.redis.hset(key, mapping=task_data)

        if ttl is not None:
            await self.set_ttl(name, ttl, prefix)

    async def get_payload(self, name: str, prefix: Optional[str] = None) -> dict:
        return await self.redis.hgetall(self._get_name(name, prefix))

    async def delete_payload(self, name: str, prefix: Optional[str] = None) -> bool:
        return await self.redis.unlink(self._get_name(name, prefix))

    async def set_ttl(self, name: str, ttl: int, prefix: Optional[str] = None):
        key = self._get_name(name, prefix)
        await self.redis.expire(key, ttl * 60)

    @staticmethod
    def _get_name(name: str, prefix: Optional[str] = None) -> str:
        if prefix is None:
            return name

        return f"{prefix}:{name}"
