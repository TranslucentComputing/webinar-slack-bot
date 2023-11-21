"""
Unit tests for Redis ETL Job.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.jobs.redis_job import IndexerJob


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("DATA_DIR", "/mocked/data/dir")


@pytest.mark.asyncio
async def test_async_run():
    """Test happy path for async_run."""
    # Mock the AsyncRedisDAOFactory and its method create_redis_dao
    with patch("src.jobs.redis_job.AsyncRedisDAOFactory") as mock_factory:
        mock_redis_dao = AsyncMock()
        mock_factory.return_value.create_redis_dao.return_value = mock_redis_dao

        # Mock file system operations
        with patch("os.listdir") as mock_listdir, patch("os.path.join") as mock_join, patch(
            "src.jobs.redis_job.logger"
        ) as mock_logger:
            mock_listdir.return_value = ["file1.csv", "file2.csv"]
            mock_join.side_effect = lambda dir, file: f"{dir}/{file}"

            # Create instance of IndexerJob
            indexer_job = IndexerJob()

            # Mock the redis_pipeline method of the IndexerJob instance
            with patch.object(
                indexer_job, "redis_pipeline", new_callable=AsyncMock
            ) as mock_redis_pipeline:
                # Execute the async_run method
                await indexer_job.async_run()

                # Assertions to verify the sequence of operations
                mock_factory.assert_called_once()
                mock_redis_dao.index_info.assert_awaited_once()
                mock_redis_dao.index_drop.assert_awaited()
                mock_redis_dao.index_create.assert_awaited_once()

                # Verify if redis_pipeline is called
                mock_redis_pipeline.assert_awaited_once_with(mock_redis_dao)

                # Verify logging calls if necessary
                mock_logger.info.assert_called()


@pytest.mark.asyncio
async def test_redis_pipeline():
    """Test happy path for redis_pipeline."""
    # Create a mock for AsyncSearchRedisDAO
    mock_redis_dao = MagicMock()
    mock_redis_dao.search_client.pipeline.return_value.__aenter__.return_value.execute = AsyncMock(
        return_value=["response"]
    )

    # Prepare the test instance of your class
    test_instance = IndexerJob()
    test_instance.csv_directory_path = "/test/path"

    # Mock os.listdir to simulate CSV files in the directory
    test_filenames = ["file1.csv", "file2.csv"]
    with patch("os.listdir", return_value=test_filenames) as mock_listdir:
        # Mock the process_file method
        with patch.object(
            test_instance, "process_file", new_callable=AsyncMock
        ) as mock_process_file:
            # Call redis_pipeline
            await test_instance.redis_pipeline(mock_redis_dao)

            # Assertions
            mock_process_file.assert_awaited()
            assert mock_process_file.call_count == len(test_filenames)
            expected_calls = [
                (
                    (
                        f"/test/path/{filename}",
                        mock_redis_dao.search_client.pipeline.return_value.__aenter__.return_value,
                    ),
                    {},
                )
                for filename in test_filenames
            ]
            mock_process_file.assert_has_awaits(expected_calls)

            # Assert pipeline execution
            pipeline_execute = (
                mock_redis_dao.search_client.pipeline.return_value.__aenter__.return_value.execute
            )
            pipeline_execute.assert_awaited_once_with(raise_on_error=True)
