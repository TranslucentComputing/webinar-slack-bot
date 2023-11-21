"""
Unit tests for SlackMiddlewareEventHandlerService.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import AsyncMock, patch

import pytest

from src.slack_bot.services.slack_middleware_eventhandler_service import (
    SlackMiddlewareEventHandlerService,
)
from src.slack_bot.services.slack_service import SlackService


@pytest.mark.asyncio
async def test_app_mention_calls_slack_service_and_sends_message():
    """
    Test that the app_mention method calls SlackService to handle the event
    and uses the say method to send a message to the correct thread.
    """

    # Mock dependencies
    mock_say = AsyncMock()
    mock_body = {"event": {"ts": "12345.67890"}}

    # Mock the SlackService.handle_event method
    with patch.object(SlackService, "handle_event", return_value=[]) as mock_handle_event:
        # Call the method
        await SlackMiddlewareEventHandlerService.app_mention(body=mock_body, say=mock_say)

        # Assertions
        mock_handle_event.assert_called_once_with(body=mock_body)
        mock_say.assert_called_once()
        assert (
            mock_say.call_args[1]["thread_ts"] == "12345.67890"
        ), "Message should be sent to the correct thread"


@pytest.mark.asyncio
async def test_app_mention_with_thread_ts():
    """
    Test that app_mention uses the thread_ts from the event body if available.
    """
    # Mock dependencies
    mock_say = AsyncMock()
    mock_body = {"event": {"ts": "12345.67890", "thread_ts": "54321.09876"}}

    # Mock the SlackService.handle_event method
    with patch.object(SlackService, "handle_event", return_value=[]) as mock_handle_event:
        # Call the method
        await SlackMiddlewareEventHandlerService.app_mention(body=mock_body, say=mock_say)

        # Assertions
        mock_handle_event.assert_called_once_with(body=mock_body)
        mock_say.assert_called_once()
        assert (
            mock_say.call_args[1]["thread_ts"] == "54321.09876"
        ), "Message should be sent to the specific thread_ts"
        mock_handle_event.assert_called_once_with(body=mock_body)
        mock_say.assert_called_once()
        assert (
            mock_say.call_args[1]["thread_ts"] == "54321.09876"
        ), "Message should be sent to the specific thread_ts"
