"""
This module provides a Data Access Object (DAO) for managing interactions
with async Redis using the async Redis Search module.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import logging
from typing import Any, Dict, List, Optional, Union

from redis.asyncio import ConnectionPool as AsyncConnectionPool
from redis.asyncio import Redis as AsyncRedis
from redis.commands.search import AsyncSearch
from redis.commands.search.field import Field
from redis.commands.search.indexDefinition import IndexDefinition
from redis.commands.search.query import Query
from redis.exceptions import ResponseError

logger = logging.getLogger("app")


class AsyncSearchRedisDAO:
    """DAO class for managing Redis search interactions.

    This class provides methods to interact with a Redis database using the Redis Search module,
    including creating, querying, and managing search indexes.

    Attributes:
        client (Redis): The Redis client instance.
        _search_client (Optional[Search]): The Redis Search client instance.
        _search_index_name (Optional[str]): The name of the search index.
    """

    def __init__(
        self,
        connection_pool: AsyncConnectionPool,
        search_index_name: str,
    ):
        """
        Initialize the Redis Search DAO with a connection pool and an optional search index name.

        Args:
            connection_pool (ConnectionPool): The connection pool to use with the Redis client.
            search_index_name (str): The name of the index used by the Search client.
        """
        self.client: AsyncRedis = AsyncRedis(connection_pool=connection_pool)

        if search_index_name is None:  # type: ignore
            raise ValueError("Search index name required.")

        self._search_client = self.client.ft(search_index_name)
        self._search_index_name = search_index_name

    @property
    def search_client(self) -> AsyncSearch:
        """
        Get the Search client from the Redis client.

        Returns:
            AsyncSearch: The Search client from the Redis client.
        """
        return self._search_client

    @property
    def search_index_name(self) -> str:
        """
        Get the name of the index used by the Search client.

        Returns:
            str: The name of the index used by the Search client.
        """
        return self._search_index_name

    async def index_info(self) -> Dict[str, Any]:
        """Get information about the search index.

        Returns:
            Dict[str, Any]: A dictionary containing information about the search index.
        """
        return await self.search_client.info()

    async def index_drop(self, delete_documents: bool = False) -> bool:
        """
        Drops the search index associated with the client.

        Args:
            delete_documents (bool, optional): If set to True, all the documents that are indexed
            are deleted along with the index. If set to False, only the index is deleted,
            not the documents. Defaults to False.

        Returns:
            bool: True if the operation was successful, False otherwise.

        Raises:
            RedisError: If there is any problem in dropping the index.

        Note:
            If you drop an index with delete_documents=False, you can recreate
            the index and reindex the
            existing documents. If delete_documents=True, you will need to add
            all the documents back to Redis.
        """
        return await self.search_client.dropindex(delete_documents=delete_documents)

    async def index_exists(self) -> bool:
        """
        Checks if the index exists in Redis.

        Returns:
            bool: True if the index exists, False otherwise.
        """
        try:
            await self.index_info()
            return True
        except ResponseError:
            return False

    async def index_create(
        self,
        fields: List[Field],
        definition: Optional[IndexDefinition] = None,
    ) -> bool:
        """
        Create an index in Redis.

        Args:
            fields (list[Union[TextField, NumericField,VectorField]]): List of TextField
                or NumericField objects.
            definition (bool, optional): Index definition. Defaults to None.
        Returns:
            None
        """
        return await self.search_client.create_index(
            fields,
            definition=definition,
        )

    async def index_search(
        self,
        query: Union[str, Query],
        query_params: Optional[dict[str, Union[str, int, float]]] = None,
    ) -> Dict[Union[bytes, str], Any]:
        """
        Executes a search query on the search index and returns the result.

        Args:
            query (Union[str, Query]): The search query. This can be a string or a Query object.
            query_params (Optional[dict[str, Union[str, int, float]]], optional): Additional
                parameters for the query. This can include parameters such as 'page_size',
                'current_page', etc. Defaults to None.

        Returns:
            Result: The result of the search query.
        """
        return await self.search_client.search(query, query_params)

    async def list_indexes(self) -> List[str]:
        """
        List all the indexes present in the Redis instance.

        Returns:
            List[str]: A list of index names.
        """
        return await self.client.execute_command("FT._LIST")

    async def add_document(
        self,
        doc_id: str,
        fields: Dict[str, Any],
        replace: bool = False,
        partial: bool = False,
        language: Optional[str] = "English",
    ) -> bool:
        """
        Adds a document to the search index.

        Args:
            doc_id (str): The unique identifier for the document.
            fields (Dict[str, Any]): The fields of the document.
            replace (bool, optional): If set to True, and the document already is in the index,
                        we perform an update and reindex the document
            partial (bool, optional): If set to True, the fields specified will be added to the
                        existing document.
                        This has the added benefit that any fields specified
                        with `no_index`
                        will not be reindexed again. Implies `replace`
            language (Optional[str], optional): The Specify the language used for
                        document tokenization. Defaults to "English".
        Returns:
            bool: True if the document was added successfully, False otherwise.
        """
        try:
            result = await self.search_client.add_document(
                doc_id=doc_id, partial=partial, replace=replace, language=language, **fields
            )

            if result is None or not isinstance(result, str):
                return False

            return result == "OK"
        except ResponseError as exc:
            logger.exception(
                "Index %s Error adding document: %s,", self._search_index_name, str(exc)
            )
            return False
