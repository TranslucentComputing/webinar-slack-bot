"""
This module provides common middleware functions.


Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import json
import logging
from typing import Any, Awaitable, Callable, Dict

from slack_bolt.async_app import AsyncSay

logger = logging.getLogger("app")


class MiddlewareCommonService:
    """Provides common middleware functionalities for Slack integration.

    This service offers middleware utilities including request logging and global error handling
    within a Slack application. It ensures that every incoming Slack request is logged for debugging
    and error analysis, and provides a unified approach to handling exceptions.
    """

    @staticmethod
    async def log_request_middleware(body: Dict[str, Any], next_: Callable[[], Awaitable[None]]):
        """
        Middleware to log Slack requests.

        Args:
            body (Dict[str, Any]): Slack request body.
            next_ (Callable[[], Awaitable[None]]): Next middleware or handler to call.
        """
        logger.debug(json.dumps(body))
        return await next_()

    @staticmethod
    async def global_error_handler(error: Exception, body: Dict[str, Any], say: AsyncSay):
        """
        Global error handler.

        Args:
            error (Exception): The raised exception.
            body (Dict[str, Any]): Slack request body.
            say (AsyncSay): Slack say function to send messages.
        """
        # log the error
        logger.exception(error)

        # Retrieve thread identifier
        event = body["event"]
        thread_ts = event.get("thread_ts", None) or event["ts"]

        # Check if the error has specific attributes like 'description' and 'status_code'
        description = getattr(error, "description", None)

        # Construct the error message
        if description:
            error_message = f"Something went wrong. Description: {description}"
        else:
            error_type = type(error).__name__
            error_summary = str(error)
            error_message = (
                f"Something went wrong. Error type: {error_type}. Error details: {error_summary}."
            )

        # Response to a specific thread with the error message
        await say(text=error_message, thread_ts=thread_ts)
