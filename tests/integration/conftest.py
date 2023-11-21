"""
This module contains setup functions called fixtures that each test will use.
Pytest automatically discovers these fixtures and injects them into your tests as needed.
Fixtures have explicit names and are activated by declaring them in your test functions
as input arguments.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import asyncio
import os
from typing import Any, Coroutine, Generator

import nest_asyncio
import pytest
from testcontainers.redis import RedisContainer

nest_asyncio.apply()

ENV_PATH = "tests/integration/.env"


@pytest.fixture(scope="module")
def load_dotenv() -> None:
    """Load environment variables from a .env file."""
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH) as f:
            for line in f:
                if line.strip() == "" or line.startswith("#"):
                    continue
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
    else:
        raise Exception(f"{ENV_PATH} does not exist.")


@pytest.fixture(scope="module")
def redis_container() -> Generator[RedisContainer, None, None]:
    """Fixture to setup and teardown Redis container"""
    with RedisContainer(image="redis/redis-stack:latest") as get_redis_container:
        yield get_redis_container


def return_awaited_value(coroutine: Coroutine[Any, Any, Any]) -> Any:
    """
    Execute the given coroutine and return its result.

    This function uses the default asyncio event loop to run the provided coroutine
    until it completes. The result of the coroutine is then returned.

    Args:
        coroutine (Coroutine[Any, Any, Any]): The coroutine to be executed.

    Returns:
        Any: The result of the awaited coroutine.

    Raises:
        Any exception that the coroutine might raise will propagate upwards.
    """
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(coroutine)
    return result
