from redis.asyncio import Redis as AsyncRedis
from redis import Redis

from common.redis.config import redis_settings

redis = Redis(**redis_settings.model_dump())
async_redis = AsyncRedis(**redis_settings.model_dump())
