import time
from fastapi import HTTPException
from redis.asyncio import Redis
from starlette.requests import Request

redis = Redis(host='book_cache', port=6379, decode_responses=True)

RATE_LIMITS = {
    "anonymous" : (2, 60),
    "authenticated" : (10, 60)
}

async def rate_limit(request:Request, user_id : str|None):
    key = str(user_id) if user_id else request.client.host
    limit_type = "authenticated" if user_id else "anonymous"
    limit, period = RATE_LIMITS[limit_type]

    now = int(time.time())
    window_start = now - period

    await redis.zremrangebyscore(key, min=0, max=window_start)
    request_count = await redis.zcard(key)
    if request_count >= limit:
        raise HTTPException(429)

    else:
        await redis.zadd( key, {str(now) : now})
        await redis.expire(key, period)


