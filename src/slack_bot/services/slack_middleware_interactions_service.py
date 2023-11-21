"""
This module provides middleware interactions service.


Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
from slack_bolt.async_app import AsyncAck, AsyncBoltContext, AsyncRespond

from config import Settings

from .slack_service import SlackService


class SlackMiddlewareInteractionsService:
    """Handles middleware interactions for Slack.

    This service is responsible for managing action handlers for button clicks
    in Slack, specifically for "good" and "bad" actions. It acknowledges
    these actions and triggers appropriate responses based on the user's choice.
    """

    @staticmethod
    async def action_good_button_click(
        ack: AsyncAck, respond: AsyncRespond, context: AsyncBoltContext
    ):
        """
        Action handler for the "good" button click in Slack.

        Args:
            ack (AsyncAck): Slack ack function to acknowledge actions.
            respond (AsyncRespond): Slack respond function to send responses.
            context (AsyncBoltContext): Slack context object.
        """

        # Return immediate response to make Slack happy
        await ack("Thanks!")

        # Retrieve settings from the context
        settings: Settings = context.get("settings")  # type: ignore

        # Create return block
        blocks = await SlackService.handle_good_interaction(settings.redis_search_index)

        # Respond with the block
        await respond(blocks=blocks)

    @staticmethod
    async def action_bad_button_click(
        ack: AsyncAck, respond: AsyncRespond, context: AsyncBoltContext
    ):
        """
        Action handler for the "bad" button click in Slack.

        Args:
            ack (AsyncAck): Slack ack function to acknowledge actions.
            respond (AsyncRespond): Slack respond function to send responses.
            context (AsyncBoltContext): Slack context object.
        """

        # Return immediate response to make Slack happy
        await ack("Thanks!")

        # Retrieve settings from the context
        settings: Settings = context.get("settings")  # type: ignore

        # Create return block
        blocks = await SlackService.handle_bad_interaction(settings.redis_search_index)

        # Respond with the block
        await respond(blocks=blocks)
