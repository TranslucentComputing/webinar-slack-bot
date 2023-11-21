"""
This module provides a factory method to create an instance of the FastAPI application.
It sets up logging, Slack integration, and health check routes.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import logging
import logging.config
from typing import Any, Dict, cast

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette_exporter import PrometheusMiddleware, handle_metrics

from config import Settings

from .exceptions.fastapi_error_handler import ErrorHandler
from .routes.slack_routes import SlackRoutes
from .services.slack_middleware import SlackMiddleware
from .utils.file_utils import load_json_file
from .utils.lifespan import lifespan
from .utils.log_filter import SuppressSpecificLogEntries


def setup_logging(fast_api: FastAPI):
    """Set up logging configurations for the app."""

    # Load the logging configuration from JSON file
    logging_config: Dict[str, Any] = cast(
        Dict[str, Any], load_json_file(fast_api.state.settings.logging_path)
    )

    # Apply the logging configuration
    logging.config.dictConfig(logging_config)

    # Set the log level
    app_logger = logging.getLogger("app")
    app_logger.setLevel(fast_api.state.settings.app_log_level.upper())

    # Add the filter to Uvicorn's access logger
    endpoints_to_suppress = ["/metrics"]

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.addFilter(SuppressSpecificLogEntries(endpoints_to_suppress))


def setup_metrics(fast_api: FastAPI):
    """Set up Prometheus middleware for the app."""
    fast_api.add_middleware(
        PrometheusMiddleware,
        group_paths=True,
        app_name="slack-bot",
        skip_paths=["/healthcheck"],
        skip_methods=["OPTIONS"],
    )

    fast_api.add_route("/metrics", handle_metrics)  # type: ignore


def setup_error_handlers(fast_api: FastAPI):
    """Set up default error handlers for the app."""
    error_handler = ErrorHandler(fast_api)
    error_handler.register_default_handlers()


def setup_routes(fast_api: FastAPI):
    """Set up general routes for the app."""

    @fast_api.get("/healthcheck")
    def health_check():
        return {"status": "Healthy"}

    @fast_api.get("/")
    def root():
        html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Welcome</title>
            </head>
            <body>
                <h1>Welcome to the Webinar!</h1>
            </body>
            </html>
            """
        return HTMLResponse(content=html_content)


def setup_slack_integration(fast_api: FastAPI):
    """Set up Slack routes and event handlers for the app."""
    slack_routes = SlackRoutes(fast_api)
    fast_api.include_router(slack_routes.get_router())

    SlackMiddleware(slack_routes.get_slack_app())


def create_app() -> FastAPI:
    """Factory method to create and return a FastAPI application instance."""

    # Create the FastAPI application
    fast_api = FastAPI(lifespan=lifespan)  # type: ignore

    # Set up the settings
    fast_api.state.settings = Settings()  # type: ignore

    # Configure the FastAPI application
    setup_logging(fast_api)
    setup_metrics(fast_api)
    setup_error_handlers(fast_api)
    setup_routes(fast_api)
    setup_slack_integration(fast_api)

    return fast_api
