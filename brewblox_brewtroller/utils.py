import asyncio
import time
from contextlib import asynccontextmanager
from datetime import timedelta
from functools import lru_cache
from typing import AsyncGenerator, Coroutine

from .models import ServiceConfig

def time_ms():
    return time.time_ns() // 1000000

@lru_cache
def get_config() -> ServiceConfig:  # pragma: no cover
    """
    Cached service configuration, loaded from env.

    Values are loaded when the model object is created.
    The same object is returned from the cache every time.

    Because values are loaded from the process env,
    this function can be called at any time.
    """
    return ServiceConfig()


@asynccontextmanager
async def task_context(coro: Coroutine,
                       cancel_timeout=timedelta(seconds=5)
                       ) -> AsyncGenerator[asyncio.Task, None]:
    task = asyncio.create_task(coro)
    try:
        yield task
    finally:
        task.cancel()
        await asyncio.wait([task], timeout=cancel_timeout.total_seconds())
