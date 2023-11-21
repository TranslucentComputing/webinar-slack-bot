"""
This module provides middleware configuration.


Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import logging

from slack_bolt.async_app import AsyncApp

from .slack_middleware_common_service import MiddlewareCommonService
from .slack_middleware_eventhandler_service import SlackMiddlewareEventHandlerService
from .slack_middleware_interactions_service import SlackMiddlewareInteractionsService

logger = logging.getLogger("app")


class SlackMiddleware:
    """Encapsulates middleware configuration.

    Attributes:
        slack_app (AsyncApp): The Slack app instance.

    Methods:
        __init__(slack_app: AsyncApp): Initializes a new SlackMiddleware instance.
    """

    def __init__(self, slack_app: AsyncApp):
        """
        Initializes a new SlackMiddleware instance.

        Args:
            slack_app (AsyncApp): The Slack app instance from `SlackRoutes`.
        """
        self.slack_app = slack_app
        self._configure_middleware()
        self._configure_error_handlers()
        self._configure_event_handlers()
        self._configure_interactions()

    def _configure_middleware(self):
        """Configures the middleware for the Slack app."""

        self.slack_app.middleware(MiddlewareCommonService.log_request_middleware)  # type: ignore

    def _configure_error_handlers(self):
        """Configures the event handlers for the Slack app."""

        self.slack_app.error(MiddlewareCommonService.global_error_handler)

    def _configure_event_handlers(self):
        """Configures the event handlers for the Slack app."""
        self.slack_app.event("app_mention")(SlackMiddlewareEventHandlerService.app_mention)  # type: ignore

    def _configure_interactions(self):
        """Configures the interactions for the Slack app."""
        self.slack_app.action("good")(SlackMiddlewareInteractionsService.action_good_button_click)  # type: ignore

        self.slack_app.action("bad")(SlackMiddlewareInteractionsService.action_bad_button_click)  # type: ignore
