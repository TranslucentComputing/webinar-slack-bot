"""
Integration Tests for AsyncSearchRedisDAO using a local Redis container.

This module contains integration tests for the AsyncSearchRedisDAO class.
It uses the testcontainers library to spin up a local Redis instance
inside a Docker container.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import uuid
from typing import Any, AsyncGenerator, Callable, Coroutine, Dict, List

import pytest
import pytest_asyncio
from pytest import FixtureRequest
from redis.commands.search.field import Field, NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from testcontainers.redis import RedisContainer

from src.slack_bot.daos.redis_dao_factory_async import AsyncRedisDAOFactory
from src.slack_bot.daos.redis_dao_search_async import AsyncSearchRedisDAO

# The type for a function that, when awaited, produces an AsyncSearchRedisDAO
DAOFactory = Callable[[], Coroutine[None, None, AsyncSearchRedisDAO]]


@pytest_asyncio.fixture(scope="function")
async def create_redis(
    request: FixtureRequest, redis_container: RedisContainer
) -> AsyncGenerator[DAOFactory, None]:
    """Fixture to provide AsyncSearchRedisDAO object."""

    teardown_clients: List[Callable[[], Coroutine[Any, Any, None]]] = []

    async def dao_factory() -> AsyncSearchRedisDAO:
        # Generate a unique index name based on the test function's name
        search_index_name = f"index_async_{request.node.name}"

        # Connection configuration
        host: str = redis_container.get_container_host_ip()
        port: int = int(redis_container.get_exposed_port(6379))
        db: int = 0
        password: str = None  # Assuming no password for the test container
        max_connections: int = 10  # Arbitrary number, adjust as needed

        # Create the DAO
        dao = AsyncRedisDAOFactory.create_redis_dao(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
            search_index_name=search_index_name,
        )

        # Assert that the returned DAO is indeed a AsyncSearchRedisDAO
        assert isinstance(dao, AsyncSearchRedisDAO), "Expected a AsyncSearchRedisDAO instance"

        async def teardown() -> None:
            await dao.client.aclose(close_connection_pool=True)

        teardown_clients.append(teardown)
        return dao

    yield dao_factory

    for teardown in teardown_clients:
        await teardown()


@pytest_asyncio.fixture(scope="function")
async def search_redis_dao(create_redis: DAOFactory) -> AsyncSearchRedisDAO:
    """Fixture to provide AsyncSearchRedisDAO object."""
    return await create_redis()


def generate_prefix() -> str:
    """Generate a unique prefix using UUID."""
    return f"{uuid.uuid4()}:"


async def create_index(dao: AsyncSearchRedisDAO, prefix: str) -> bool:
    """Helper function to create an index."""
    fields: List[Field] = [TextField("title"), NumericField("price")]
    return await dao.index_create(
        fields=fields,
        definition=IndexDefinition(index_type=IndexType.HASH, prefix=[prefix]),
    )


async def add_document(
    dao: AsyncSearchRedisDAO, document: Dict[str, Any], prefix: str = None
) -> bool:
    """Helper function to add a document to the index."""
    if prefix is None:
        prefix = generate_prefix()
    return await dao.add_document(f"{prefix}doc{dao.search_index_name}_{uuid.uuid4()}", document)


@pytest.mark.asyncio
async def test_search_redis_add_index(search_redis_dao: AsyncSearchRedisDAO):
    """Test AsyncSearchRedisDAO add_index functionality."""

    # Create index
    prefix = generate_prefix()
    assert await create_index(search_redis_dao, prefix)

    # Verify if the index has been created
    indices = await search_redis_dao.list_indexes()

    # Use the search_index_name attribute of the search_redis_dao to get the index name
    assert search_redis_dao.search_index_name in indices


@pytest.mark.asyncio
@pytest.mark.usefixtures("search_redis_dao")
async def test_search_redis_search_document(search_redis_dao: AsyncSearchRedisDAO):
    """Test AsyncSearchRedisDAO search functionality."""

    # Setup query and data
    query = "Test product"
    document: Dict[str, Any] = {"title": "Test product", "price": 19.99}

    # Create an index
    prefix = generate_prefix()
    assert await create_index(search_redis_dao, prefix)

    # Add a document to the index
    assert await add_document(search_redis_dao, document, prefix)

    # Query the index
    result: Dict[str, Any] = await search_redis_dao.index_search(query)
    results: List[Dict[str, Any]] = result["results"]
    extra_attributes: Dict[str, Any] = results[0]["extra_attributes"]

    assert result["total_results"] == 1
    assert extra_attributes["title"] == document["title"]
    assert extra_attributes["price"] == str(document["price"])


@pytest.mark.asyncio
@pytest.mark.usefixtures("search_redis_dao")
async def test_search_redis_drop_index(search_redis_dao: AsyncSearchRedisDAO):
    """Test AsyncSearchRedisDAO drop_index functionality."""

    # Create an index
    prefix = generate_prefix()
    assert await create_index(search_redis_dao, prefix)

    # Drop the index
    assert await search_redis_dao.index_drop()

    # Verify if the index has been deleted
    indices = await search_redis_dao.list_indexes()
    assert search_redis_dao.search_index_name not in indices


@pytest.mark.asyncio
@pytest.mark.usefixtures("search_redis_dao")
async def test_search_redis_index_info(search_redis_dao: AsyncSearchRedisDAO):
    """Test AsyncSearchRedisDAO index_info functionality."""

    # Create an index
    prefix = generate_prefix()
    assert await create_index(search_redis_dao, prefix)

    # Retrieve index info
    info = await search_redis_dao.index_info()
    assert "index_name" in info
    assert info["index_name"] == search_redis_dao.search_index_name


@pytest.mark.asyncio
@pytest.mark.usefixtures("search_redis_dao")
async def test_search_redis_multiple_documents(search_redis_dao: AsyncSearchRedisDAO):
    """Test adding and searching multiple documents."""

    # Create an index
    prefix = generate_prefix()
    assert await create_index(search_redis_dao, prefix)

    # Add multiple documents
    documents = [
        {"title": "Product A", "price": 19.99},
        {"title": "Product B", "price": 29.99},
        {"title": "Product C", "price": 39.99},
    ]
    for doc in documents:
        assert await add_document(search_redis_dao, doc, prefix)

    # Search and verify all documents are returned
    result: Dict[str, Any] = await search_redis_dao.index_search("Product")
    assert result["total_results"] == 3


@pytest.mark.asyncio
@pytest.mark.usefixtures("search_redis_dao")
async def test_search_redis_non_existent_document(search_redis_dao: AsyncSearchRedisDAO):
    """Test searching for a non-existent document."""

    # Create an index and add a document
    prefix = generate_prefix()
    assert await create_index(search_redis_dao, prefix)
    assert await add_document(
        search_redis_dao, {"title": "Existing Product", "price": 19.99}, prefix
    )

    # Search for a non-existent document
    result: Dict[str, Any] = await search_redis_dao.index_search("Non-existent Product")
    results: List[Dict[str, Any]] = result["results"]

    assert len(results) == 0
    assert result["total_results"] == 0


@pytest.mark.asyncio
@pytest.mark.usefixtures("search_redis_dao")
async def test_search_redis_partial_matches(search_redis_dao: AsyncSearchRedisDAO):
    """Test searching with partial matches."""

    # Create an index and add a document
    prefix = generate_prefix()
    assert await create_index(search_redis_dao, prefix)
    assert await add_document(
        search_redis_dao, {"title": "Specialized Product", "price": 19.99}, prefix
    )

    # Search using a part of the document's content
    result: Dict[str, Any] = await search_redis_dao.index_search("Special")
    results: List[Dict[str, Any]] = result["results"]
    extra_attributes: Dict[str, Any] = results[0]["extra_attributes"]

    assert extra_attributes["title"] == "Specialized Product"


@pytest.mark.asyncio
@pytest.mark.usefixtures("search_redis_dao")
async def test_search_redis_update_document(search_redis_dao: AsyncSearchRedisDAO):
    """Test updating and searching an updated document."""

    # Create an index and add a document
    prefix = generate_prefix()
    assert await create_index(search_redis_dao, prefix)

    doc_id = f"{prefix}doc{search_redis_dao.search_index_name}_{uuid.uuid4()}"

    # Add a document
    assert await search_redis_dao.add_document(doc_id, {"title": "Old Product", "price": 19.99})

    # Update the document
    assert await search_redis_dao.add_document(
        doc_id, {"title": "Updated Product", "price": 29.99}, partial=True
    )

    # Search and verify the updated document is returned
    result: Dict[str, Any] = await search_redis_dao.index_search("Updated Product")
    results: List[Dict[str, Any]] = result["results"]
    extra_attributes: Dict[str, Any] = results[0]["extra_attributes"]

    assert extra_attributes["title"] == "Updated Product"
    assert extra_attributes["price"] == str(29.99)
