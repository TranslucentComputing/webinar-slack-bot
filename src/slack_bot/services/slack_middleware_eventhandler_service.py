"""
This module provides middleware event handler service.


Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from typing import Any, Dict, Optional, Sequence, Union

from slack_bolt.async_app import AsyncSay
from slack_sdk.models.blocks import Block

from .slack_service import SlackService


class SlackMiddlewareEventHandlerService:
    """Handles event-based interactions for Slack.

    This service is designed to manage event handlers for specific Slack events,
    particularly app mentions. It processes the event data and responds appropriately
    within the context of the mentioned thread.
    """

    @staticmethod
    async def app_mention(body: Dict[str, Any], say: AsyncSay):
        """
        Event handler for app mentions in Slack.

        Args:
            body (Dict[str, Any]): Slack event body.
            say (AsyncSay): Slack say function to send messages.
            context (AsyncBoltContext): Slack context object.
        """

        # Retrieve thread identifier
        event = body["event"]
        thread_ts = event.get("thread_ts", None) or event["ts"]

        # Handle event
        blocks: Optional[Sequence[Union[Dict[str, Any], Block]]] = await SlackService.handle_event(
            body=body
        )

        # Send message to a specific thread
        await say(text="Response", blocks=blocks, thread_ts=thread_ts)
