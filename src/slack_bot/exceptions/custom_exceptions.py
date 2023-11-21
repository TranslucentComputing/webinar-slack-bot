"""
Custom exception classes for the project.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from typing import Any, Optional


class Error(Exception):
    """Base class for other exceptions"""

    status_code = 500
    description = "An unexpected error occurred."

    def __init__(self, *args: object, description: Optional[str] = None) -> None:
        """Initialize Error instance.

        Allows for a custom description that describes the error.

        Args:
            *args: Variable length argument list.
            description: An optional custom description of the error.
        """
        super().__init__(*args)
        if description is not None:
            self.description = description


class BusinessLogicError(Error):
    """Base class for exceptions in business logic."""

    status_code = 400
    description = "A business logic error occurred."


class SlackServiceError(BusinessLogicError):
    """Custom exception for errors during Slack Service operations."""


class SlackMissingEventTypeError(BusinessLogicError):
    """Exception raised when the event type is missing in the payload."""


class InvalidJsonDataError(BusinessLogicError):
    """Exception raised when the JSON data is invalid."""


class IndexingError(Error):
    """Raised when there's an error during the indexing process."""


class JSONFileError(Exception):
    """Base exception for errors related to reading JSON files."""

    def __init__(self, message_format: str, *args: Any):
        message = message_format % args
        super().__init__(message)


class JSONFileNotFoundError(JSONFileError):
    """Raised when the JSON file is not found."""

    def __init__(self, filename: str):
        super().__init__("JSON File '%s' not found.", filename)


class JSONInvalidError(JSONFileError):
    """Raised when the JSON file is invalid."""

    def __init__(self, filename: str, error: str):
        super().__init__("JSON File '%s' is not a valid JSON. Error: %s", filename, error)


class JSONInvalidEncodingError(JSONFileError):
    """Raised when the file encoding is not UTF-8."""

    def __init__(self, filename: str, error: str):
        super().__init__(
            "JSON File '%s' does not use valid utf-8 encoding. Error: %s", filename, error
        )


class CSVFileReadError(Exception):
    """Custom exception for handling CSV file read errors."""
