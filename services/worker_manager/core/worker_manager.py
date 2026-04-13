from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

from core.dependencies import singleton


@dataclass
class WorkerInfo:
    worker_id: str  # This is also the name of the queue.
    created_at: datetime
    last_heartbeat: datetime
    current_load: int = 0
    max_load: int = 3
    status: str = "active"  # active, busy, offline


@singleton
class WorkerManager:
    def __init__(self):
        self.workers: Dict[str, WorkerInfo] = {}
        self._lock = asyncio.Lock()

    async def register_worker(self, worker_id: str) -> None:
        async with self._lock:
            self.workers[worker_id] = WorkerInfo(
                worker_id=worker_id,
                created_at=datetime.now(),
                last_heartbeat=datetime.now()
            )

    async def update_worker_load(self, worker_id: str, load: int) -> None:
        async with self._lock:
            if worker_id in self.workers:
                self.workers[worker_id].current_load = load
                self.workers[worker_id].last_heartbeat = datetime.now()

    async def get_available_worker(self) -> Optional[WorkerInfo]:
        async with self._lock:
            available_workers = [
                w for w in self.workers.values()
                if w.status == "active" and w.current_load < w.max_load
            ]
            if available_workers:
                return min(available_workers, key=lambda w: w.current_load)
            return None

    async def remove_worker(self, worker_id: str) -> None:
        async with self._lock:
            self.workers.pop(worker_id, None)
