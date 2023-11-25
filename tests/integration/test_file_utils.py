"""
Integration tests for for JSON file utility functions.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""

import logging
import os
import tempfile

import chardet
import pytest

logger = logging.getLogger(__name__)

from src.slack_bot.utils.file_utils import (
    JSONFileNotFoundError,
    JSONInvalidEncodingError,
    JSONInvalidError,
    load_json_file,
)

data_dir = os.path.join(os.path.dirname(__file__), "data")


def test_load_valid_json_file():
    """Integration test to ensure load_json_file correctly loads a valid JSON file."""

    # Construct the full path to the valid JSON file
    valid_json_path = os.path.join(data_dir, "valid.json")

    # Load and assert the expected data
    expected_data = {
        "name": "John Doe",
        "age": 30,
        "isEmployed": True,
    }
    assert load_json_file(valid_json_path) == expected_data


def test_load_nonexistent_json_file():
    """Integration test to check if JSONFileNotFoundError is raised for a non-existent file."""
    with pytest.raises(JSONFileNotFoundError):
        load_json_file("nonexistent.json")


def test_load_invalid_json_file():
    """Integration test to verify JSONInvalidError is raised for an invalid JSON file."""
    with pytest.raises(JSONInvalidError):
        load_json_file(os.path.join(data_dir, "invalid.json"))


def get_file_encoding(file_path: str):
    """Determine the encoding of the given file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The detected encoding of the file.
    """
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
        return encoding


def test_load_non_utf8_json_file():
    """Integration test to confirm JSONInvalidEncodingError is raised for a non-UTF-8 encoded file."""

    non_utf8_data = '{"key": "Café"}'  # Non-ASCII character
    with tempfile.NamedTemporaryFile(mode="w", encoding="ISO-8859-1", delete=False) as temp_file:
        temp_file.write(non_utf8_data)
        temp_filename = temp_file.name

    encoding = get_file_encoding(temp_filename)
    logger.info("The encoding of the file is: %s", encoding)

    with pytest.raises(JSONInvalidEncodingError):
        load_json_file(temp_filename)
