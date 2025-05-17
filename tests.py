from fastapi import HTTPException
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from starlette.requests import Request
from app.rate_limit import rate_limit


async def rate_limit_test(zcard_return, username=None):
    mock_redis = AsyncMock()
    mock_redis.zcard.return_value = zcard_return

    with patch("app.rate_limit.redis", mock_redis):
        request = MagicMock(spec=Request)
        request.client.host = "127.0.0.1"

        try:
            await rate_limit(request, username)
        except HTTPException as e:
            return e.status_code
        else:
            return 200

@pytest.mark.asyncio
async def test_1():
    # Тестимо для неавторизованого користувача, із невикористаним лімітом
    assert await rate_limit_test(1) == 200

@pytest.mark.asyncio
async def test_2():
    # Тестимо для неавторизованого користувача, із вичерпаним лімітом
    assert await rate_limit_test(3) == 429

@pytest.mark.asyncio
async def test_3():
    # Тестимо для авторизованого користувача, із невикористаним лімітом
    assert await rate_limit_test(3, 'taras') == 200

@pytest.mark.asyncio
async def test_4():
    # Тестимо для авторизованого користувача, із використаним лімітом
    assert await rate_limit_test(11, 'taras') == 429