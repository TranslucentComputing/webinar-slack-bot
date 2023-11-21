"""
Unit tests for log filter.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import logging
from typing import List

import pytest

from src.slack_bot.utils.log_filter import SuppressSpecificLogEntries


@pytest.mark.parametrize(
    "message, suppressed_entries, expected_result",
    [
        ("This is a debug message.", ["suppress_me", "ignore_this"], True),
        ("This should suppress_me.", ["suppress_me", "ignore_this"], False),
        ("This is a warning.", ["suppress_me", "ignore_this"], True),
        ("Do not ignore_this error.", ["suppress_me", "ignore_this"], False),
    ],
)
def test_suppress_specific_log_entries_parametrized(
    message: str, suppressed_entries: List[str], expected_result: bool
):
    """
    Tests the SuppressSpecificLogEntries filter.

    Args:
        message (str): The message to be tested.
        suppressed_entries (List[str]): The list of strings to be suppressed.
        expected_result (bool): The expected result.
    """
    suppress_filter = SuppressSpecificLogEntries(suppressed_entries)
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg=message,
        args=None,
        exc_info=None,
    )
    assert suppress_filter.filter(record) == expected_result


def test_suppress_specific_log_entries():
    """Tests the SuppressSpecificLogEntries filter with logger."""

    # Create a logger instance
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)

    # Add the SuppressSpecificLogEntries filter
    logger.addFilter(SuppressSpecificLogEntries(["suppress_me", "ignore_this"]))

    # Define a list to collect log messages
    log_messages: List[str] = []

    # Define a custom handler to collect log messages
    class ListHandler(logging.Handler):
        """A custom handler to collect log messages"""

        def emit(self, record):
            log_messages.append(record.getMessage())

    logger.addHandler(ListHandler())

    # Log some messages
    logger.debug("This is a debug message.")
    logger.info("This should suppress_me.")
    logger.warning("This is a warning.")
    logger.error("Do not ignore_this error.")

    # Check the collected log messages
    assert log_messages == ["This is a debug message.", "This is a warning."]
