"""
Unit test for the async redis search dao.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import AsyncMock, MagicMock

import pytest
from redis.commands.search.field import NumericField, TextField
from redis.exceptions import ResponseError

from src.slack_bot.daos.redis_dao_search_async import AsyncSearchRedisDAO

SEARCH_INDEX_NAME = "test_index"  # Define a constant for the search index name


@pytest.fixture
def redis_search_dao() -> AsyncSearchRedisDAO:
    """Create a AsyncSearchRedisDAO mock with a mock Redis and Search client."""

    # Create a AsyncSearchRedisDAO instance with a mocked connection pool
    connection_pool_mock = MagicMock()
    search_dao = AsyncSearchRedisDAO(connection_pool_mock, SEARCH_INDEX_NAME)

    # Set the mock Redis client and mock Search client in the AsyncSearchRedisDAO instance
    search_dao.client = AsyncMock()
    search_dao._search_client = AsyncMock()

    return search_dao


@pytest.mark.asyncio
async def test_index_info(redis_search_dao: AsyncSearchRedisDAO):
    """Tests the index_info method of the AsyncSearchRedisDAO object."""

    # Act
    await redis_search_dao.index_info()

    # Assert: Check that 'info' was called once on 'search_client'
    redis_search_dao.search_client.info.assert_called_once()


@pytest.mark.asyncio
async def test_index_drop(redis_search_dao: AsyncSearchRedisDAO):
    """Tests the index_drop method of the AsyncSearchRedisDAO object."""

    # Act
    await redis_search_dao.index_drop(delete_documents=False)

    # Assert: Verify that 'dropindex' was called correctly on 'search_client'
    redis_search_dao.search_client.dropindex.assert_called_once_with(delete_documents=False)


@pytest.mark.asyncio
async def test_index_exists(redis_search_dao: AsyncSearchRedisDAO):
    """
    Test the 'index_exists' method of the AsyncSearchRedisDAO object.

    This test verifies that the 'index_exists' method correctly calls the
    'info' method on the 'search_client' mock to check the existence of the index.
    """

    # Act: Call the 'index_exists' method
    await redis_search_dao.index_exists()

    # Assert: Check that 'info' was called once on 'search_client'
    redis_search_dao.search_client.info.assert_called_once()


@pytest.mark.asyncio
async def test_index_exists_response_error(redis_search_dao: AsyncSearchRedisDAO):
    """
    Test the 'index_exists' method of the AsyncSearchRedisDAO object when a
    ResponseError is raised.

    This test ensures that 'index_exists' returns False when a ResponseError
    is encountered during the 'info' call on the 'search_client'.
    """

    # Arrange: Mock 'info' to raise ResponseError
    redis_search_dao.search_client.info = AsyncMock(side_effect=ResponseError)

    # Act: Call the 'index_exists' method and capture the result
    result = await redis_search_dao.index_exists()

    # Assert: Verify the result is False and 'info' was called once
    assert result is False
    redis_search_dao.search_client.info.assert_called_once()


@pytest.mark.asyncio
async def test_index_exists_no_error(redis_search_dao: AsyncSearchRedisDAO):
    """
    Test the 'index_exists' method of the AsyncSearchRedisDAO object when no error is raised.

    This test checks that 'index_exists' returns True when no errors are
    encountered during the 'info' call on the 'search_client'.
    """

    # Arrange: Mock 'info' method
    redis_search_dao.search_client.info = AsyncMock()

    # Act: Call 'index_exists' and capture the result
    result = await redis_search_dao.index_exists()

    # Assert: Verify the result is True and 'info' was called once
    assert result is True
    redis_search_dao.search_client.info.assert_called_once()


@pytest.mark.asyncio
async def test_index_create(redis_search_dao: AsyncSearchRedisDAO):
    """
    Test the 'index_create' method of the AsyncSearchRedisDAO object.

    This test ensures that 'index_create' correctly invokes the 'create_index'
    method on the 'search_client' with the given fields.
    """

    # Arrange: Define fields for the index
    fields = [TextField("field1"), NumericField("field2")]

    # Act: Call the 'index_create' method with the fields
    await redis_search_dao.index_create(fields=fields)

    # Assert: Verify 'create_index' was called correctly on 'search_client'
    redis_search_dao.search_client.create_index.assert_called_once_with(fields, definition=None)
