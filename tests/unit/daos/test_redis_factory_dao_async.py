"""
Unit test for the async redis factory dao.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import patch

import pytest
from redis.asyncio import ConnectionPool

from src.slack_bot.daos.redis_dao_factory_async import AsyncRedisDAOFactory
from src.slack_bot.daos.redis_dao_search_async import AsyncSearchRedisDAO

MOCK_CONNECTION_POOL = (
    "src.slack_bot.daos.redis_dao_factory_async.AsyncRedisDAOFactory._connection_pool"
)


def test_get_connection_pool():
    """Test the get_connection_pool method."""
    # Arrange - Setup for the test
    with patch(
        MOCK_CONNECTION_POOL,
        None,
    ):
        # Act - Perform the action being tested
        pool = AsyncRedisDAOFactory.get_connection_pool("localhost", 6379, 0, "password", 10)

        # Assert - Verify the result
        assert isinstance(pool, ConnectionPool)


def test_connection_pool_creation():
    """Test the connection pool creation."""
    # Arrange & Act
    pool1 = AsyncRedisDAOFactory.get_connection_pool("localhost", 6379, 0, "password", 10)
    pool2 = AsyncRedisDAOFactory.get_connection_pool("localhost", 6379, 0, "password", 10)

    # Assert
    assert pool1 is pool2


def test_multiple_dao_creations():
    """Test multiple dao creations."""
    # Arrange & Act
    dao1 = AsyncRedisDAOFactory.create_redis_dao(
        host="localhost",
        port=6379,
        db=0,
        password="password",
        max_connections=10,
        search_index_name="test",
    )

    # Assert
    assert isinstance(dao1, AsyncSearchRedisDAO)


def test_create_redis_dao_with_existing_pool_without_existing_pool():
    """Test the create_redis_dao_with_existing_pool method without an existing pool."""
    # Arrange
    with patch(
        MOCK_CONNECTION_POOL,
        None,
    ):
        # Act & Assert
        with pytest.raises(
            ValueError,
            match="No existing connection pool found. Initialize the connection pool first.",
        ):
            AsyncRedisDAOFactory.create_redis_dao_with_existing_pool(search_index_name="test")


def test_create_redis_dao_with_existing_pool_no_pool():
    """Test the create_redis_dao_with_existing_pool method without an existing pool."""
    # Arrange - Patch the connection pool to be None
    with patch(
        "src.slack_bot.daos.redis_dao_factory_async.AsyncRedisDAOFactory._connection_pool",
        None,
    ):
        # Act & Assert - Expect a ValueError when trying to create DAO without a pool
        with pytest.raises(ValueError):
            AsyncRedisDAOFactory.create_redis_dao_with_existing_pool(search_index_name="test")


def test_create_redis_dao_with_existing_pool_with_pool():
    """Test create_redis_dao_with_existing_pool method with an existing pool."""
    # Arrange - Create a mock connection pool
    AsyncRedisDAOFactory._connection_pool = ConnectionPool(
        host="localhost", port=6379, db=0, password="password", max_connections=10
    )

    # Act - Create a DAO with the existing pool
    dao = AsyncRedisDAOFactory.create_redis_dao_with_existing_pool(search_index_name="test")

    # Assert - Check if the DAO is an instance of AsyncSearchRedisDAO
    assert isinstance(dao, AsyncSearchRedisDAO)


def test_dao_properties():
    """Test the dao properties."""
    # Arrange & Act - Create a DAO
    dao = AsyncRedisDAOFactory.create_redis_dao(
        host="localhost",
        port=6379,
        db=0,
        password="password",
        max_connections=10,
        search_index_name="test_index",
    )

    # Assert - Check DAO's properties
    assert dao.client.connection_pool is not None
    assert dao.search_index_name == "test_index"


def test_create_redis_dao_search_without_index():
    """Test create_redis_dao method without providing a search index name."""
    # Arrange & Act & Assert - Expect ValueError when creating DAO without index name
    with pytest.raises(ValueError):
        AsyncRedisDAOFactory.create_redis_dao(
            host="localhost",
            port=6379,
            db=0,
            password="password",
            max_connections=10,
        )


def test_create_redis_dao_search_with_index():
    """Test create_redis_dao method with a search index name."""
    # Arrange & Act - Create a DAO with a search index name
    dao = AsyncRedisDAOFactory.create_redis_dao(
        host="localhost",
        port=6379,
        db=0,
        password="password",
        max_connections=10,
        search_index_name="test_index",
    )

    # Assert - Verify the DAO's properties
    assert isinstance(dao, AsyncSearchRedisDAO)
    assert dao.search_index_name == "test_index"
