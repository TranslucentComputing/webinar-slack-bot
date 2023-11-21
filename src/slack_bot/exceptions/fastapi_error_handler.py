"""
ErrorHandler module.

Handles HTTP and custom exceptions using FastAPI's exception handler mechanism.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from typing import Callable, Type, Union

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .custom_exceptions import Error


class CustomJSONResponse(JSONResponse):
    """Custom JSONResponse class."""

    def __init__(self, status_code: int, name: str, description: str) -> None:
        # Validate status_code
        if status_code is None or not (100 <= status_code < 600):
            status_code = 500

        content = {"code": status_code, "name": name, "description": description}
        super().__init__(status_code=status_code, content=content)


class ErrorHandler:
    """
    ErrorHandler class to manage HTTP and custom exceptions.

    Attributes:
        app (FastAPI): The FastAPI application instance.

    Methods:
        _base_error_handler(request, exc): Handle base custom errors.
        _http_exception_handler(request, exc): Handle HTTPException errors.
        add_exception_handler(exception, handler): Register an exception handler to the FastAPI app.
        register_default_handlers(): Register default exception handlers for the app.
    """

    def __init__(self, app: FastAPI):
        """
        Initialize ErrorHandler instance.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        self.app = app

    def _base_error_handler(self, request: Request, exc: Error) -> CustomJSONResponse:
        """
        Handle base custom errors.

        Args:
            request (Request): The request that caused the exception.
            exc (Error): The raised custom error instance.

        Returns:
            CustomJSONResponse: A formatted JSON response with error details.
        """
        return CustomJSONResponse(
            status_code=exc.status_code, name=type(exc).__name__, description=exc.description
        )

    def _http_exception_handler(self, request: Request, exc: HTTPException) -> CustomJSONResponse:
        """
        Handle HTTPException errors.

        Args:
            request (Request): The request that caused the exception.
            exc (HTTPException): The raised HTTPException instance.

        Returns:
            CustomJSONResponse: A formatted JSON response with error details.
        """
        return CustomJSONResponse(
            status_code=exc.status_code, name=type(exc).__name__, description=exc.detail
        )

    def add_exception_handler(
        self, exception: Union[int, Type[Exception]], handler: Callable
    ) -> None:
        """
        Register an exception handler to the FastAPI app.

        Args:
            exception (Union[int, Type[Exception]]): The exception type to handle.
            handler (Callable): The function to execute when the exception occurs.
        """
        self.app.add_exception_handler(exception, handler)

    def register_default_handlers(self) -> None:
        """
        Register default exception handlers for the app.
        """
        self.add_exception_handler(HTTPException, self._http_exception_handler)
        self.add_exception_handler(Error, self._base_error_handler)
