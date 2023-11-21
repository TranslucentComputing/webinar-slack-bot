"""
Unit tests for FastAPI Configuration.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from src.slack_bot import (
    create_app,
    setup_error_handlers,
    setup_logging,
    setup_metrics,
    setup_routes,
    setup_slack_integration,
)
from src.slack_bot.services.slack_middleware import SlackMiddleware


@pytest.fixture
def mock_fast_api() -> FastAPI:
    """Create FastAPI object for testing."""
    app = FastAPI()
    app.state.settings = MagicMock()
    return app


def test_setup_logging(mock_fast_api: FastAPI):
    """Test configuration of logging."""
    with patch("src.slack_bot.load_json_file") as mock_load_json, patch(
        "logging.config.dictConfig"
    ) as mock_dict_config, patch("logging.getLogger") as mock_get_logger:
        mock_load_json.return_value = {"version": 1}  # Mock expected config
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        setup_logging(mock_fast_api)

        mock_load_json.assert_called_once()
        mock_dict_config.assert_called_once()
        mock_get_logger.assert_any_call("app")
        mock_logger.setLevel.assert_called_once()


def test_setup_metrics(mock_fast_api: FastAPI):
    """Test configuration of metrics."""
    with patch("src.slack_bot.PrometheusMiddleware"):
        setup_metrics(mock_fast_api)
        assert "/metrics" in [route.path for route in mock_fast_api.routes]


def test_setup_error_handlers(mock_fast_api: FastAPI):
    """Test configuration of error handlers."""
    setup_error_handlers(mock_fast_api)

    # Assert that a handler for HTTPException has been added
    assert HTTPException in mock_fast_api.exception_handlers

    # Assert that a handler for RequestValidationError has been added
    assert RequestValidationError in mock_fast_api.exception_handlers


def test_setup_routes(mock_fast_api: FastAPI):
    """Test configuration of basic routes."""
    setup_routes(mock_fast_api)
    assert "/healthcheck" in [route.path for route in mock_fast_api.routes]
    assert "/" in [route.path for route in mock_fast_api.routes]


def test_setup_slack_integration(mock_fast_api: FastAPI):
    """Test configuration of slack routes."""
    with patch("src.slack_bot.SlackRoutes") as routes, patch(
        "src.slack_bot.SlackMiddleware"
    ) as middleware:
        setup_slack_integration(mock_fast_api)

        # Assert SlackRoutes class was used
        routes.assert_called_once()

        # Assert SlackMiddleware class was used
        middleware.assert_called_once()


def test_create_app():
    """Test creating FastAPI with config."""
    with patch("src.slack_bot.setup_logging"), patch("src.slack_bot.setup_metrics"), patch(
        "src.slack_bot.setup_error_handlers"
    ), patch("src.slack_bot.setup_routes"), patch("src.slack_bot.setup_slack_integration"):
        app = create_app()
        assert isinstance(app, FastAPI)
