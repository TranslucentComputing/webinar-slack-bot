"""
Unit tests for for JSON file utility functions.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from unittest.mock import mock_open, patch

import pytest

from src.slack_bot.utils.file_utils import (
    JSONFileError,
    JSONFileNotFoundError,
    JSONInvalidEncodingError,
    JSONInvalidError,
    load_json_file,
)


def test_module_exists():
    """Test if the File Utils module exists"""
    try:
        import src.slack_bot.utils.file_utils
    except ImportError:
        pytest.fail("file_utils module does not exist")


def test_load_json_file_function_exists():
    """Test if the add function exists in the file_utils module"""
    try:
        from src.slack_bot.utils.file_utils import load_json_file

        assert callable(load_json_file), "load_json_file function is not callable"
    except ImportError:
        pytest.fail("load_json_file function does not exist in file_utils module")


def test_load_valid_json_file():
    """Test that the load_json_file function loads a valid json file."""
    m = mock_open(read_data='{"key": "value"}')
    with patch("builtins.open", m):
        result = load_json_file("dummy_path.json")
        assert result == {"key": "value"}


def test_load_complex_json_file():
    """Test that the load_json_file function loads a complex json file."""
    m = mock_open(read_data='{"key1": {"subkey1": ["value1", "value2"]}, "key2": true}')
    with patch("builtins.open", m):
        result = load_json_file("complex_file.json")
        assert result == {"key1": {"subkey1": ["value1", "value2"]}, "key2": True}


def test_load_file_unexpected_error():
    """Test that the load_json_file function raises a general error for unexpected issues."""
    with patch("builtins.open", side_effect=PermissionError()):
        with pytest.raises(JSONFileError):
            load_json_file("no_permission.json")


def test_load_nonexistent_file():
    """Test that the load_json_file function raises an error for a nonexistent file."""
    with patch("builtins.open", side_effect=FileNotFoundError()):
        with pytest.raises(JSONFileNotFoundError):
            load_json_file("nonexistent.json")


def test_load_empty_file():
    """Test that the load_json_file function raises an error for an empty json file."""
    m = mock_open(read_data="")
    with patch("builtins.open", m):
        with pytest.raises(JSONInvalidError):
            load_json_file("empty_file.json")


def test_load_invalid_json_file():
    """Test that the load_json_file function raises an error for an invalid json file."""
    m = mock_open(read_data="{key: value}")
    with patch("builtins.open", m):
        with pytest.raises(JSONInvalidError):
            load_json_file("dummy_path.json")


def test_file_with_different_encoding():
    """Test that the load_json_file function raises an error for a file with the wrong encoding."""
    data = '{"key": "á"}'
    m = mock_open(read_data=data.encode("latin-1"))
    with patch(
        "builtins.open", m, create=True
    ):  # `create=True` since we're patching a different signature
        with pytest.raises(JSONInvalidEncodingError):
            load_json_file("encoded_file.json")
