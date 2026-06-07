import redis
import os
import json
from datetime import timedelta

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_client = redis.Redis.from_url(
        REDIS_URL, 
        decode_responses=True,
        socket_timeout=1,
        socket_connect_timeout=1
    )
    # Ping it once to ensure we fail fast on startup if not available
    redis_client.ping()
except Exception:
    redis_client = None

def get_cache(key: str):
    if not redis_client:
        return None
    try:
        data = redis_client.get(key)
        return json.loads(data) if data else None
    except Exception:
        return None

def set_cache(key: str, value: dict, expire_seconds: int = 3600):
    if not redis_client:
        return
    try:
        redis_client.setex(key, timedelta(seconds=expire_seconds), json.dumps(value))
    except Exception:
        pass

def delete_cache(pattern: str):
    if not redis_client:
        return
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass
