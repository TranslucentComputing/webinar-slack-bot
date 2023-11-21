"""
Unit tests for SlackService.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from slack_sdk.models.blocks import (
    ActionsBlock,
    Block,
    ButtonElement,
    MarkdownTextObject,
    PlainTextObject,
    SectionBlock,
    TextObject,
)

from src.slack_bot.services.slack_service import SlackService


@pytest.mark.asyncio
async def test_handle_event_with_wake_up_message():
    """Test trigger phrase."""
    body = {"event": {"text": "wake up", "user": "U12345"}}
    response = await SlackService.handle_event(body)
    assert response is not None
    assert len(response) == 2  # Expecting 2 blocks

    block_1: Block = response[0]  # type: ignore

    assert isinstance(block_1, SectionBlock)

    block_2: Block = response[1]  # type: ignore

    assert isinstance(block_2, ActionsBlock)
    assert len(block_2.elements) == 2

    button_1 = block_2.elements[0]
    assert isinstance(button_1, ButtonElement)

    assert button_1.action_id == "good"

    button_2 = block_2.elements[1]
    assert isinstance(button_2, ButtonElement)

    assert button_2.action_id == "bad"


@pytest.mark.asyncio
async def test_handle_event_with_no_wake_up_message():
    """Test regular response."""
    body = {"event": {"text": "random text", "user": "U12345"}}
    response = await SlackService.handle_event(body)
    assert response is not None
    assert len(response) == 1  # Expecting 1 block

    block_1: Block = response[0]  # type: ignore

    assert isinstance(block_1, SectionBlock)
    assert "Sleeeeeping" in block_1.text.text  # type: ignore


@pytest.mark.asyncio
@patch("src.slack_bot.services.slack_service.AsyncRedisDAOFactory")
async def test_get_quote_with_results(mock_factory: MagicMock):
    """Test get_quote method."""
    mock_dao = AsyncMock()
    mock_factory.create_redis_dao_with_existing_pool.return_value = mock_dao
    mock_dao.index_search.side_effect = [
        {"total_results": 1},  # First call for total results
        {
            "results": [{"extra_attributes": {"quote": "Test Quote", "person": "Test Person"}}]
        },  # Second call for random entry
    ]

    quote = await SlackService.get_quote("search_index")
    assert quote == ("Test Quote", "Test Person")


@pytest.mark.asyncio
@patch("src.slack_bot.services.slack_service.AsyncRedisDAOFactory")
async def test_get_quote_with_no_results(mock_factory: MagicMock):
    """Test get_quote method with no results."""
    mock_dao = AsyncMock()
    mock_factory.create_redis_dao_with_existing_pool.return_value = mock_dao
    mock_dao.index_search.return_value = {"total_results": 0}

    quote = await SlackService.get_quote("search_index")
    assert quote is None


@pytest.mark.asyncio
@patch("src.slack_bot.services.slack_service.SlackService.get_quote")
async def test_handle_good_interaction_with_quote(mock_get_quote: MagicMock):
    """Test good interaction with a quote."""
    mock_get_quote.return_value = ("Test Quote", "Test Person")
    response = await SlackService.handle_good_interaction("search_index")
    assert response is not None
    assert len(response) == 2  # Expecting 2 blocks


@pytest.mark.asyncio
@patch("src.slack_bot.services.slack_service.SlackService.get_quote")
async def test_handle_good_interaction_without_quote(mock_get_quote: MagicMock):
    """Test good interaction without a quote."""
    mock_get_quote.return_value = None
    response = await SlackService.handle_good_interaction("search_index")
    assert response is not None
    assert len(response) == 1  # Expecting 1 block


@pytest.mark.asyncio
@patch("src.slack_bot.services.slack_service.SlackService.get_quote")
async def test_handle_bad_interaction_with_quote(mock_get_quote: MagicMock):
    """Test bad interaction with a quote."""
    mock_get_quote.return_value = ("Test Quote", "Test Person")
    response = await SlackService.handle_bad_interaction("search_index")
    assert response is not None
    assert len(response) == 2  # Expecting 2 blocks


@pytest.mark.asyncio
@patch("src.slack_bot.services.slack_service.SlackService.get_quote")
async def test_handle_bad_interaction_without_quote(mock_get_quote: MagicMock):
    """Test bad interaction without a quote."""
    mock_get_quote.return_value = None
    response = await SlackService.handle_bad_interaction("search_index")
    assert response is not None
    assert len(response) == 1  # Expecting 1 block
