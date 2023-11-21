"""
This module provides routes that handle Slack events and interactions.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""

import logging

from fastapi import APIRouter, FastAPI, Request
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_bolt.async_app import AsyncApp

logger = logging.getLogger("app")


class SlackRoutes:
    """Encapsulates routes for Slack interactions and events.

    Attributes:
        settings (Settings): FastAPI app settings.
        slack_app (AsyncApp): The Slack app instance.
        app_handler (AsyncSlackRequestHandler): Slack request handler.
        router (APIRouter): The FastAPI router for these routes.

    Methods:
        get_router() -> APIRouter:
            Returns the configured router for the Slack routes.
    """

    def __init__(self, app: FastAPI):
        """
        Initializes a new SlackRoutes instance.

        Args:
            app (FastAPI): The main FastAPI app instance.
        """
        if not hasattr(app, "state") or not hasattr(app.state, "settings"):
            raise ValueError("The app settings are not set.")

        self.settings = app.state.settings

        self.slack_app = AsyncApp(
            token=self.settings.slack_bot_token,
            signing_secret=self.settings.slack_signing_secret,
            logger=logger,
        )

        self.app_handler = AsyncSlackRequestHandler(self.slack_app)

        self.router = APIRouter()
        self._configure_routes()

    def _configure_routes(self):
        """Configures the Slack routes and attaches them to the router."""

        @self.router.post("/slack/events")
        async def endpoint_events(req: Request):
            """
            Endpoint for Slack events.

            Args:
                req (Request): The incoming request from FastAPI.

            Returns:
                Any: The result from the Slack request handler.
            """
            return await self.app_handler.handle(req, {"settings": self.settings})

        @self.router.post("/slack/interactions")
        async def endpoint_interactions(req: Request):
            """
            Endpoint for Slack interactions.

            Args:
                req (Request): The incoming request from FastAPI.

            Returns:
                Any: The result from the Slack request handler.
            """
            return await self.app_handler.handle(req, {"settings": self.settings})

    def get_router(self) -> APIRouter:
        """
        Retrieves the router configured with the Slack routes.

        Returns:
            APIRouter: The router configured with Slack routes.
        """
        return self.router

    def get_slack_app(self) -> AsyncApp:
        """
        Retrieves the Slack app instance.

        Returns:
            AsyncApp: The Slack app instance.
        """
        return self.slack_app
