from dataclasses import dataclass
import json
from typing import Any, final

import structlog
from redis.asyncio import Redis
import redis.exceptions

from {{cookiecutter.project_slug}}.application.interfaces.cache import CacheProtocol

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class RedisCacheClient(CacheProtocol):
    client: Redis
    ttl: int | None = None

    async def get(self, key: str) -> Any | None:
        try:
            value = await self.client.get(key)
            if value is None:
                return None
            return json.loads(value)
        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error(
                "Redis get operation failed", key=key, error=str(e)
            )
            return None
        except (json.JSONDecodeError, TypeError) as e:
            logger.warning(
                "Failed to decode cached value", key=key, error=str(e)
            )
            return None

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        try:
            serialized_value = json.dumps(value, default=str)
            if ttl is not None:
                await self.client.setex(key, ttl, serialized_value)
            elif self.ttl is not None:
                await self.client.setex(key, self.ttl, serialized_value)
            else:
                await self.client.set(key, serialized_value)
            return True
        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error(
                "Redis set operation failed", key=key, error=str(e)
            )
            return False
        except (TypeError, ValueError) as e:
            logger.error(
                "Failed to serialize value for cache",
                key=key,
                error=str(e),
            )
            return False

    async def delete(self, key: str) -> bool:
        try:
            result = await self.client.delete(key)
            return result > 0
        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error(
                "Redis delete operation failed", key=key, error=str(e)
            )
            return False

    async def exists(self, key: str) -> bool:
        try:
            return bool(await self.client.exists(key))
        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error(
                "Redis exists operation failed", key=key, error=str(e)
            )
            return False

    async def clear(self, pattern: str) -> int:
        try:
            keys = []
            async for key in self.client.scan_iter(match=pattern):
                keys.append(key)
            if keys:
                deleted_count = await self.client.delete(*keys)
                logger.info(
                    "Cleared cache keys matching pattern",
                    pattern=pattern,
                    count=deleted_count,
                )
                return deleted_count
            return 0
        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error(
                "Redis clear pattern operation failed",
                pattern=pattern,
                error=str(e),
            )
            return 0

    async def close(self) -> None:
        try:
            await self.client.close()
            logger.info("Redis connection closed")
        except (ConnectionError, redis.exceptions.RedisError) as e:
            logger.error("Failed to close Redis connection", error=str(e))
