"""
Unit tests for MiddlewareCommonService.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import json
from unittest.mock import AsyncMock

import pytest
from pytest import LogCaptureFixture

from src.slack_bot.services.slack_middleware_common_service import MiddlewareCommonService


@pytest.mark.asyncio
async def test_log_request_middleware_logs_request_body(caplog: LogCaptureFixture):
    """Test that the log_request middleware logs the Slack request body."""
    test_body = {"test": "data"}
    next_ = AsyncMock()

    # Directly call the middleware function
    await MiddlewareCommonService.log_request_middleware(body=test_body, next_=next_)

    # Assert log was made
    assert json.dumps(test_body) in caplog.text


@pytest.mark.asyncio
async def test_global_error_handler_logs_exception_and_sends_message(caplog: LogCaptureFixture):
    """Test that the global error handler logs the exception and sends a message."""
    test_body = {"event": {"ts": "12345"}}
    test_error = Exception("Test error")
    mock_say = AsyncMock()

    # Directly call the error handler function
    await MiddlewareCommonService.global_error_handler(test_error, test_body, mock_say)

    # Assert say was called with an error message
    assert mock_say.called, "The say function was not called"

    # Check if the error message contains the expected text
    assert (
        "Test error" in mock_say.call_args[1]["text"]
    ), "Error message did not contain expected text"

    # Assert the exception was logged
    assert "Test error" in caplog.text, "The exception was not logged correctly"


@pytest.mark.asyncio
async def test_global_error_handler_with_description():
    """
    Test that the global error handler sends a message with the error description
    if present in the exception.
    """

    class CustomException(Exception):
        """Test Exception"""

        def __init__(self, message: str, description: str):
            super().__init__(message)
            self.description = description

    test_body = {"event": {"ts": "12345"}}
    test_description = "A custom error occurred"
    test_error = CustomException("Test error", test_description)
    mock_say = AsyncMock()

    # Directly call the error handler function
    await MiddlewareCommonService.global_error_handler(test_error, test_body, mock_say)

    # Assert say was called with an error message
    assert mock_say.called, "The say function was not called"

    # Assert say was called with a message that contains the custom description
    error_message = mock_say.call_args[1]["text"]
    assert test_description in error_message, "Error message did not contain expected description"
