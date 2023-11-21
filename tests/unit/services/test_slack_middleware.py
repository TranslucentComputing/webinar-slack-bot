"""
Unit tests for Slack middleware.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import AsyncMock

import pytest
from slack_bolt.async_app import AsyncApp

from src.slack_bot.services.slack_middleware import SlackMiddleware


@pytest.fixture
def mock_slack_app() -> AsyncMock:
    """Fixture to create a mock SlackApp instance."""
    return AsyncMock(spec=AsyncApp)


def test_init_configures_middleware_and_event_handlers(mock_slack_app: AsyncMock):
    """Test that middleware, event handlers, error handlers, and interactions
    are configured on initialization.
    """
    SlackMiddleware(mock_slack_app)

    # Test that middleware is configured
    assert mock_slack_app.middleware.called, "Middleware should be configured"

    # Test that error handlers are configured
    assert mock_slack_app.error.called, "Error handlers should be configured"

    # Test that event handlers are configured
    assert mock_slack_app.event.called, "Event handlers should be configured"

    # Test that interactions are configured
    assert mock_slack_app.action.called, "Interaction handlers should be configured"


def test_configure_middleware_registers_correct_middleware(mock_slack_app: AsyncMock):
    """Test that the correct middleware is registered."""
    SlackMiddleware(mock_slack_app)

    # Check if the log_request_middleware is registered
    assert (
        mock_slack_app.middleware.call_args[0][0].__name__ == "log_request_middleware"
    ), "log_request_middleware should be registered"


def test_configure_error_handlers_registers_global_error_handler(mock_slack_app: AsyncMock):
    """Test that the global error handler is registered."""
    SlackMiddleware(mock_slack_app)

    # Check if the global_error_handler is registered
    assert (
        mock_slack_app.error.call_args[0][0].__name__ == "global_error_handler"
    ), "global_error_handler should be registered"


def test_configure_event_handlers_registers_app_mention_handler(mock_slack_app: AsyncMock):
    """Test that the app mention event handler is registered."""
    SlackMiddleware(mock_slack_app)

    # Check if the app_mention event handler is registered
    assert any(
        call[0][0] == "app_mention" for call in mock_slack_app.event.call_args_list
    ), "App mention event handler should be registered"


def test_configure_interactions_registers_action_handlers(mock_slack_app: AsyncMock):
    """Test that the action handlers for 'good' and 'bad' are registered."""
    SlackMiddleware(mock_slack_app)

    # Check if the action handlers for 'good' and 'bad' are registered
    action_calls = [call[0][0] for call in mock_slack_app.action.call_args_list]
    assert "good" in action_calls, "'Good' action handler should be registered"
    assert "bad" in action_calls, "'Bad' action handler should be registered"
