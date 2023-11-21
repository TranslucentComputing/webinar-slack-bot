"""
Tests for the FastAPI exception handling using the ErrorHandler class.

This module contains pytest fixtures and test cases for the custom exception handlers
in the FastAPI application. It tests both HTTPException-based errors and custom errors
raised during the API's operation.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from src.slack_bot.exceptions.custom_exceptions import Error
from src.slack_bot.exceptions.fastapi_error_handler import ErrorHandler


@pytest.fixture(scope="module")
def test_app() -> FastAPI:
    """
    Fixture to create a FastAPI application instance.

    Returns:
        FastAPI: The FastAPI application instance.
    """
    app = FastAPI()

    @app.get("/http_exception")
    def http_exception_endpoint():
        raise HTTPException(status_code=404, detail="Not Found")

    @app.get("/custom_error")
    def custom_error_endpoint():
        raise Error(description="Custom Error")

    return app


@pytest.fixture(scope="module")
def test_client(test_app: FastAPI) -> TestClient:
    """
    Fixture to create a FastAPI test client instance.

    Returns:
        TestClient: The FastAPI test client instance.
    """
    return TestClient(test_app)


@pytest.fixture(scope="module")
def error_handler(test_app: FastAPI) -> ErrorHandler:
    """
    Fixture to create an ErrorHandler instance.

    Returns:
        ErrorHandler: The ErrorHandler instance.
    """
    return ErrorHandler(test_app)


def test_http_exception_handler(test_client: TestClient, error_handler: ErrorHandler):
    """Test the HTTPException exception handler."""
    error_handler.register_default_handlers()
    response = test_client.get("/http_exception")
    assert response.status_code == 404
    assert response.json() == {"code": 404, "description": "Not Found", "name": "HTTPException"}


def test_base_error_handler(test_client: TestClient, error_handler: ErrorHandler):
    """Test the base custom error handler."""
    error_handler.register_default_handlers()
    response = test_client.get("/custom_error")
    assert response.status_code == 500
    assert response.json() == {"code": 500, "description": "Custom Error", "name": "Error"}
