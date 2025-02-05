# src/ai_service/cache/redis_cache.py
# Copyright (c) 2023 Your Company. All rights reserved.

import redis

def connect_to_redis(host: str, port: int) -> redis.Redis:
    """
    Connect to a Redis server.

    Args:
        host (str): The Redis server host.
        port (int): The Redis server port.

    Returns:
        redis.Redis: The Redis connection object.
    """
    return redis.Redis(host=host, port=port)

class CodeCache:
    def get(self, prompt_hash: str) -> Optional[str]:
        return self.redis.get(f"codegen:{prompt_hash}")
