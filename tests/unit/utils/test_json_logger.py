"""
Unit tests for JSON formatter extension.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import json
import logging
from logging import LogRecord

import pytest
from pythonjsonlogger import jsonlogger

from src.slack_bot.utils.json_logger import JsonFormatter


@pytest.fixture
def log_record() -> LogRecord:
    """Create a log record for testing."""
    logger = logging.getLogger("test")
    record = LogRecord(
        name=logger.name,
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test log message",
        args=(),
        exc_info=None,
    )

    # Add the 'color_message' attribute to the record
    record.color_message = "Colored Message for Testing"

    return record


def test_json_formatter_excludes_reserved_attrs(log_record: LogRecord):
    """Test that the JsonFormatter correctly excludes reserved attributes."""
    formatter = JsonFormatter()
    formatted = formatter.format(log_record)

    # Convert the formatted string back to a dictionary
    log_dict = json.loads(formatted)

    # Ensure the 'color_message' attribute is not present
    assert (
        "color_message" not in log_dict
    ), "The 'color_message' attribute should not be in the formatted output"


def test_json_formatter_includes_standard_attrs(log_record: LogRecord):
    """Test that the JsonFormatter includes standard log record attributes."""
    formatter = JsonFormatter()
    formatted = formatter.format(log_record)

    # Convert the formatted string back to a dictionary
    log_dict = json.loads(formatted)

    # Check for standard attributes
    assert "message" in log_dict, "The 'message' attribute should be in the formatted output"


def test_json_formatter_custom_format(log_record: LogRecord):
    """Test that the JsonFormatter respects custom format strings."""
    custom_format = "%(asctime)s %(levelname)s %(message)s"
    formatter = JsonFormatter(custom_format)
    formatted = formatter.format(log_record)

    # Convert the formatted string back to a dictionary
    log_dict = json.loads(formatted)

    # Check for attributes in custom format
    assert "asctime" in log_dict, "The 'asctime' attribute should be in the formatted output"
    assert "levelname" in log_dict, "The 'levelname' attribute should be in the formatted output"
    assert "message" in log_dict, "The 'message' attribute should be in the formatted output"
    assert "asctime" in log_dict, "The 'asctime' attribute should be in the formatted output"
    assert "levelname" in log_dict, "The 'levelname' attribute should be in the formatted output"
    assert "message" in log_dict, "The 'message' attribute should be in the formatted output"
