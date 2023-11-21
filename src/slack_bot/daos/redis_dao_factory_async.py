"""
This module provides an async factory class for managing the creation
of different types of async Redis Data Access Objects (DAOs).

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import logging
from typing import Optional

from redis.asyncio import ConnectionPool, RedisError

from .redis_dao_search_async import AsyncSearchRedisDAO

logger = logging.getLogger("app")


class AsyncRedisDAOFactory:
    """Factory class for managing dao creation."""

    _connection_pool: Optional[ConnectionPool] = None

    @classmethod
    def get_connection_pool(
        cls,
        host: str,
        port: int,
        db: int,
        password: str,
        max_connections: int,
        decode_responses: bool = True,
    ) -> ConnectionPool:
        """Create and return a Redis connection pool if it doesn't exist,
        otherwise return the existing one.

        Args:
            host (str): Redis host address.
            port (int): Redis port.
            db (int): Redis database number.
            password (str): Redis password.
            max_connections (int): Max connections for Redis.

        Returns:
            ConnectionPool: Redis connection pool object.
        """
        if cls._connection_pool is None:
            try:
                cls._connection_pool = ConnectionPool(
                    host=host,
                    port=port,
                    db=db,
                    password=password,
                    decode_responses=decode_responses,
                    max_connections=max_connections,
                    protocol=3,  # Using protocol 3 with version 5 or Redis lib.
                )
            except RedisError as exc:
                logger.error("Failed to create a Redis connection pool: %s", exc)
                raise exc
        return cls._connection_pool

    @classmethod
    async def reset_connection_pool(cls) -> None:
        """Reset the connection pool and log the reset action."""
        if cls._connection_pool is not None:
            await cls._connection_pool.aclose()
            cls._connection_pool = None
        logger.info("Connection pool reset.")

    @classmethod
    def _dao(
        cls,
        connection_pool: ConnectionPool,
        search_index_name: Optional[str] = None,
    ) -> AsyncSearchRedisDAO:
        """
        Choose and return the appropriate DAO based on the dao_type.

        Args:
            connection_pool (ConnectionPool): The connection pool to use for the DAO.
            search_index_name (Optional[str]): The name of the index used by the Search client.

        Returns:
            AsyncSearchRedisDAO: DAO object based on the specified type.

        Raises:
            ValueError: If an invalid search index name provided.
        """
        if search_index_name is None:
            raise ValueError("Search index name not provided.")
        return AsyncSearchRedisDAO(
            connection_pool=connection_pool,
            search_index_name=search_index_name,
        )

    @classmethod
    def create_redis_dao_with_existing_pool(
        cls, search_index_name: Optional[str] = None
    ) -> AsyncSearchRedisDAO:
        """
        Create and return a new DAO object using the existing connection pool.

        Args:
            search_index_name (Optional[str], optional): The name of the index used by the Search
                client. If not provided, the Search client will not be initialized.

        Raises:
            ValueError: If no connection pool has been created yet or
                if an invalid dao_type is provided.

        Returns:
            AsyncSearchRedisDAO: DAO object based on the specified type.
        """
        if cls._connection_pool is None:
            raise ValueError(
                "No existing connection pool found. Initialize the connection pool first."
            )

        return cls._dao(cls._connection_pool, search_index_name)

    @classmethod
    def create_redis_dao(
        cls,
        host: str,
        port: int,
        db: int,
        password: str,
        max_connections: int,
        search_index_name: Optional[str] = None,
        decode_responses: bool = True,
    ) -> AsyncSearchRedisDAO:
        """
        Create and return a new DAO object using a new connection pool or existing one.

        Args:
            host (str): Redis host address.
            port (int): Redis port.
            db (int): Redis database number.
            password (str): Redis password.
            max_connections (int): Max connections for Redis.
            search_index_name (Optional[str], optional): The name of the index used by the Search
                client. If not provided, the Search client will not be initialized.
            decode_responses (bool, optional): Whether to decode responses from Redis.

        Raises:
            ValueError: If an invalid dao_type is provided.

        Returns:
            AsyncSearchRedisDAO: DAO object based on the specified type.
        """
        connection_pool = cls.get_connection_pool(
            host, port, db, password, max_connections, decode_responses
        )

        return cls._dao(connection_pool, search_index_name)
