"""
Indexer Job Module.

Provides an ETL job implementation for indexing CSV files into a Redis Search index.

This module contains the `IndexerJob` class, which extends the functionality of the
`ETLJob` class to specifically handle the extraction of data from CSV files and
its indexing into a Redis database.

Classes:
    IndexerJob: Extends the ETLJob to implement CSV file indexing into Redis.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import csv
import logging
import os
import sys
from datetime import datetime
from typing import Any, List, Optional

from redis.commands.search import AsyncPipeline
from redis.commands.search.field import Field, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import RedisError

from ..slack_bot.daos.redis_dao_factory_async import AsyncRedisDAOFactory
from ..slack_bot.daos.redis_dao_search_async import AsyncSearchRedisDAO
from ..slack_bot.exceptions.custom_exceptions import CSVFileReadError
from .etl_config import ETLSettings
from .etl_job import ETLJob

logger = logging.getLogger("etl")


class IndexerJob(ETLJob):
    """
    A class used to read and index CSV files into a Redis database.

    This class is an implementation of an ETL job that focuses on the extraction of
    data from CSV files and loading it into a Redis Search index. It uses an asynchronous
    approach to handle potentially large datasets efficiently.

    Methods:
        async_run: Executes the indexing job asynchronously.
    """

    def __init__(self):
        """
        Initializes the IndexerJob with Redis configurations and the path to the JSONL file.
        """
        super().__init__()

        logger.setLevel(logging.DEBUG)

        # Create a StreamHandler for stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)

        # Optionally set a formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stdout_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(stdout_handler)

        self.etl_settings: ETLSettings = ETLSettings()

        data_dir: Optional[str] = os.environ.get("DATA_DIR", None)
        if data_dir is None:
            raise ValueError("DATA_DIR environment variable is required.")
        self.csv_directory_path = data_dir
        self.prefix = f'{datetime.now().strftime("%Y%m%d%H%M%S")}:'

    def run(self) -> None:
        """
        Not implemented for asynchronous job.

        Raises:
            NotImplementedError: Always, as this method is not implemented.
        """
        raise NotImplementedError("The synchronous run method is not implemented for this job.")

    async def async_run(self) -> None:
        """
        Executes the indexing job asynchronously.
        """

        # create the Redis DAO
        redis_dao = AsyncRedisDAOFactory().create_redis_dao(
            search_index_name=self.etl_settings.redis_search_index,
            host=self.etl_settings.redis_host,
            port=self.etl_settings.redis_port,
            db=self.etl_settings.redis_db,
            password=self.etl_settings.redis_password,
            max_connections=self.etl_settings.redis_max_connections,
            decode_responses=False,
        )

        # Fields
        redis_fields: List[Field] = [TextField("quote"), TextField("person")]

        try:
            # check to see if index exists
            await redis_dao.index_info()
            logger.info("Index already exists!")
            await redis_dao.index_drop(delete_documents=True)
            logger.info("Deleted!")
        except:
            logger.info("Index does not exists!")

        # create index
        await redis_dao.index_create(
            redis_fields,
            definition=IndexDefinition(prefix=[self.prefix], index_type=IndexType.HASH),
        )

        # process the files
        await self.redis_pipeline(
            redis_dao,
        )

    async def redis_pipeline(self, redis_dao: AsyncSearchRedisDAO):
        """Execute redis pipeline on the CSV files."""
        try:
            async with redis_dao.search_client.pipeline(transaction=True) as pipe:
                for filename in os.listdir(self.csv_directory_path):
                    if filename.endswith(".csv"):
                        await self.process_file(
                            os.path.join(self.csv_directory_path, filename), pipe
                        )
                res: List[Any] = await pipe.execute(raise_on_error=True)
                logger.info("Processed %s documents", len(res))
        except RedisError as exc:
            logger.error("Error adding vectors to Redis: %s", str(exc))

    async def process_file(self, filepath: str, redis_pipeline: AsyncPipeline) -> None:
        """
        Processes a single CSV file and adds its contents to the Redis pipeline.

        Args:
            filepath: The path of the file to process.
            redis_pipeline: The Redis pipeline object for batch operations.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                csv_reader = csv.DictReader(file)
                for idx, row in enumerate(csv_reader):
                    key = f"{self.prefix}_{os.path.basename(filepath)}_{idx}"
                    redis_pipeline.hset(  # type: ignore
                        key, mapping={"quote": row["Quote"], "person": row["Person"]}
                    )
        except IOError as exc:
            raise CSVFileReadError(f"Failed to read {filepath} : {str(exc)}") from exc


if __name__ == "__main__":
    IndexerJob.async_execute()
