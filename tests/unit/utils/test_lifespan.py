"""
Unit tests for FatAPI lifespan protocol function.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from typing import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI

from config import Settings
from src.slack_bot.utils.lifespan import lifespan


@pytest.fixture
def mock_app() -> FastAPI:
    """Create FastAPI object for testing."""
    app = FastAPI()
    app.state.settings = Settings()  # type: ignore
    return app


@pytest.fixture
def mock_async_redis_dao_factory() -> Generator[MagicMock, None, None]:
    """Mock the Redis DAO factor."""
    with patch("src.slack_bot.utils.lifespan.AsyncRedisDAOFactory") as mock_factory:
        mock_factory.get_connection_pool = AsyncMock()
        mock_factory.reset_connection_pool = AsyncMock()
        yield mock_factory


@pytest.mark.asyncio
async def test_lifespan_context_manager(mock_app: FastAPI, mock_async_redis_dao_factory: MagicMock):
    """
    Test the lifespan context manager function for the FastAPI application.

    This test checks if the Redis connection pool is correctly initialized and
    closed during the application's lifespan.
    """
    async with lifespan(mock_app) as life:
        assert life is None  # Check that the context manager yields None

    # Assert that get_connection_pool was called with the correct parameters
    mock_async_redis_dao_factory.get_connection_pool.assert_called_once_with(
        host=mock_app.state.settings.redis_host,
        port=mock_app.state.settings.redis_port,
        db=mock_app.state.settings.redis_db,
        password=mock_app.state.settings.redis_password,
        max_connections=mock_app.state.settings.redis_max_connections,
    )

    # Assert that reset_connection_pool was called once
    mock_async_redis_dao_factory.reset_connection_pool.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan_context_manager_with_no_settings(mock_app: FastAPI):
    """
    Test the lifespan context manager function when app settings are not set.

    This test checks if the lifespan context manager raises a ValueError when
    the FastAPI application's settings are not configured.
    """
    mock_app.state.settings = None  # Simulate no settings

    with pytest.raises(ValueError) as exc_info:
        async with lifespan(mock_app):
            pass

    assert "The app settings are not set." in str(exc_info.value)
