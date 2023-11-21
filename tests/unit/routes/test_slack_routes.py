"""
Unit tests for Slack routes.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from typing import Optional
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import APIRouter, FastAPI
from pytest_mock import MockerFixture
from slack_bolt.async_app import AsyncApp
from starlette.routing import Route

from src.slack_bot.routes.slack_routes import SlackRoutes


@pytest.fixture
def mock_app() -> FastAPI:
    """Fixture to create a mock FastAPI app with settings."""
    app = FastAPI()
    app.state.settings = MagicMock()  # Mock the settings
    return app


@pytest.fixture
def app_without_settings() -> FastAPI:
    """Create a FastAPI app instance without settings."""
    return FastAPI()


@pytest.fixture
def mock_request() -> AsyncMock:
    """Fixture to create a mock request object."""
    return AsyncMock()


@pytest.fixture
def mock_handler(mocker: MockerFixture) -> AsyncMock:
    """Mock the AsyncSlackRequestHandler."""
    mock = AsyncMock()
    mocker.patch("src.slack_bot.routes.slack_routes.AsyncSlackRequestHandler", return_value=mock)
    return mock


@pytest.fixture
def slack_routes(mock_app: FastAPI, mock_handler: AsyncMock) -> SlackRoutes:
    """Fixture to create a SlackRoutes instance."""
    return SlackRoutes(mock_app)


def test_slack_routes_initialization(mock_app: FastAPI):
    """Test the initialization of SlackRoutes."""
    # Arrange & Act
    slack_routes = SlackRoutes(mock_app)

    # Assert
    assert slack_routes.settings is mock_app.state.settings
    assert slack_routes.slack_app is not None
    assert slack_routes.app_handler is not None
    assert slack_routes.router is not None


def test_slack_routes_init_without_settings(app_without_settings: FastAPI):
    """
    Test that initializing SlackRoutes without app settings raises ValueError.
    """
    with pytest.raises(ValueError) as exc_info:
        SlackRoutes(app_without_settings)

    assert str(exc_info.value) == "The app settings are not set."


def find_route_by_path(router: APIRouter, path: str) -> Optional[Route]:
    """Find a route in the router by its path."""
    for route in router.routes:
        assert isinstance(route, Route)
        if route.path == path:
            return route
    return None


@pytest.mark.asyncio
async def test_endpoint_events(
    mocker: MockerFixture,
    slack_routes: SlackRoutes,
    mock_request: AsyncMock,
    mock_handler: AsyncMock,
):
    """Test the /slack/events endpoint."""

    # Arrange
    mock_handler.handle = mocker.AsyncMock()
    route: Optional[Route] = find_route_by_path(slack_routes.router, "/slack/events")

    # Act
    assert route is not None, "Route /slack/events not found"
    response = await route.endpoint(mock_request)

    # Assert
    mock_handler.handle.assert_called_once_with(mock_request, {"settings": slack_routes.settings})
    assert response is not None


@pytest.mark.asyncio
async def test_endpoint_interactions(
    mocker: MockerFixture,
    slack_routes: SlackRoutes,
    mock_request: AsyncMock,
    mock_handler: AsyncMock,
):
    """Test the /slack/interactions endpoint."""
    # Arrange
    mock_handler.handle = mocker.AsyncMock()
    route: Optional[Route] = find_route_by_path(slack_routes.router, "/slack/interactions")

    # Act
    assert route is not None, "Route /slack/interactions not found"
    response = await route.endpoint(mock_request)

    # Assert
    mock_handler.handle.assert_called_once_with(mock_request, {"settings": slack_routes.settings})
    assert response is not None


def test_get_router_returns_configured_router(slack_routes: SlackRoutes):
    """Test to verify that get_router returns the configured APIRouter."""
    # Act
    router = slack_routes.get_router()

    # Assert
    assert router is not None
    assert isinstance(router, APIRouter)


def test_get_slack_app_returns_slack_app_instance(slack_routes: SlackRoutes):
    """Test to verify that get_slack_app returns the Slack app instance."""
    # Act
    slack_app = slack_routes.get_slack_app()

    # Assert
    assert slack_app is not None
    assert isinstance(slack_app, AsyncApp)
    assert isinstance(slack_app, AsyncApp)
