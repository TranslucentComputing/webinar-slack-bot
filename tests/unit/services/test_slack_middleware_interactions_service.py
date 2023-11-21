"""
Unit tests for SlackMiddlewareInteractionsService.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from slack_bolt.async_app import AsyncBoltContext

from config import Settings
from src.slack_bot.services.slack_middleware_interactions_service import (
    SlackMiddlewareInteractionsService,
)
from src.slack_bot.services.slack_service import SlackService


@pytest.mark.asyncio
async def test_action_good_button_click():
    """
    Test that the action_good_button_click method acknowledges the action,
    retrieves settings, and sends a response.
    """
    mock_ack = AsyncMock()
    mock_respond = AsyncMock()
    mock_context = AsyncMock(AsyncBoltContext, get=MagicMock(return_value=Settings()))

    # Mock the SlackService.handle_good_interaction method
    with patch.object(SlackService, "handle_good_interaction", return_value=[]):
        await SlackMiddlewareInteractionsService.action_good_button_click(
            mock_ack, mock_respond, mock_context
        )

        mock_ack.assert_called_once_with("Thanks!")
        mock_context.get.assert_called_once_with("settings")
        mock_respond.assert_called_once()


@pytest.mark.asyncio
async def test_action_bad_button_click():
    """
    Test that the action_bad_button_click method acknowledges the action,
    retrieves settings, and sends a response.
    """
    mock_ack = AsyncMock()
    mock_respond = AsyncMock()
    mock_context = AsyncMock(AsyncBoltContext, get=MagicMock(return_value=Settings()))

    # Mock the SlackService.handle_bad_interaction method
    with patch.object(SlackService, "handle_bad_interaction", return_value=[]):
        await SlackMiddlewareInteractionsService.action_bad_button_click(
            mock_ack, mock_respond, mock_context
        )

        mock_ack.assert_called_once_with("Thanks!")
        mock_context.get.assert_called_once_with("settings")
        mock_respond.assert_called_once()
