"""
Unit tests for the custom errors.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import pytest

from src.slack_bot.exceptions.custom_exceptions import (
    BusinessLogicError,
    Error,
    InvalidJsonDataError,
    SlackMissingEventTypeError,
    SlackServiceError,
)


def test_base_error():
    """Test the base Error class with default description."""

    try:
        raise Error()
    except Error as exc:
        assert str(exc) == ""
        assert exc.description == "An unexpected error occurred."


def test_base_error_with_description():
    """Test the base Error class with a custom description."""

    try:
        raise Error(description="A custom error occurred.")
    except Error as exc:
        assert str(exc) == ""
        assert exc.description == "A custom error occurred."


def test_error_base_class():
    """Test error base class"""
    with pytest.raises(Error) as excinfo:
        raise Error("Test error")

    assert str(excinfo.value) == "Test error"
    assert excinfo.value.status_code == 500
    assert excinfo.value.description == "An unexpected error occurred."


def test_error_base_class_custom_description():
    """Test error base class with custom description"""
    with pytest.raises(Error) as excinfo:
        raise Error("Test error", description="Custom description")
    assert str(excinfo.value) == "Test error"
    assert excinfo.value.status_code == 500
    assert excinfo.value.description == "Custom description"


def test_missing_event_type_error():
    """Test missing event type error"""
    with pytest.raises(SlackMissingEventTypeError) as excinfo:
        raise SlackMissingEventTypeError("Missing event type error")
    assert str(excinfo.value) == "Missing event type error"


def test_invalid_json_data_error():
    """Test invalid JSON data error"""
    with pytest.raises(InvalidJsonDataError) as excinfo:
        raise InvalidJsonDataError("Invalid JSON data error")
    assert str(excinfo.value) == "Invalid JSON data error"


def test_business_logic_error():
    """Test business logic error"""
    with pytest.raises(BusinessLogicError) as excinfo:
        raise BusinessLogicError("Business logic error")
    assert str(excinfo.value) == "Business logic error"
    assert excinfo.value.status_code == 400
    assert excinfo.value.description == "A business logic error occurred."


def test_business_logic_error_custom_description():
    """Test business logic error with custom description"""
    with pytest.raises(BusinessLogicError) as excinfo:
        raise BusinessLogicError("Business logic error", description="Custom description")
    assert str(excinfo.value) == "Business logic error"
    assert excinfo.value.status_code == 400
    assert excinfo.value.description == "Custom description"


def test_slack_service_error():
    """Test slack service error"""
    with pytest.raises(SlackServiceError) as excinfo:
        raise SlackServiceError("Slack service error")
    assert str(excinfo.value) == "Slack service error"
    assert excinfo.value.status_code == 400
    assert excinfo.value.description == "A business logic error occurred."


def test_slack_service_error_custom_description():
    """Test slack service error with custom description"""
    with pytest.raises(SlackServiceError) as excinfo:
        raise SlackServiceError("Slack service error", description="Custom description")
    assert str(excinfo.value) == "Slack service error"
    assert excinfo.value.status_code == 400
    assert excinfo.value.description == "Custom description"
