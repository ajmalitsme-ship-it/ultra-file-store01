import redis
import time
from core.config import REDIS_URL

redis_client = redis.from_url(REDIS_URL)


def check_rate(key: str, limit: int = 10, period: int = 60) -> bool:

    now = int(time.time())
    window = now // period

    redis_key = f"rate:{key}:{window}"

    current = redis_client.get(redis_key)

    if current and int(current) >= limit:
        return False

    redis_client.incr(redis_key)
    redis_client.expire(redis_key, period)

    return True
