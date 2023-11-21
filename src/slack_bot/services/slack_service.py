"""
This module provides a service to handle Slack events, process the input from a Slack message,
and respond to the input by interacting with the OpenAI service and Redis storage.

Author: Patryk Golabek
Company: Translucent Computing Inc.
Copyright: 2023 Translucent Computing Inc.
"""
import logging
import random
from typing import Any, Dict, Optional, Sequence, Tuple, Union

from redis.commands.search.query import Query
from slack_sdk.models.blocks import (
    ActionsBlock,
    Block,
    ButtonElement,
    MarkdownTextObject,
    PlainTextObject,
    SectionBlock,
    TextObject,
)

from ..daos.redis_dao_factory_async import AsyncRedisDAOFactory

logger = logging.getLogger("app")


class SlackService:
    """Service class to handle Slack events and interactions."""

    @staticmethod
    async def handle_event(
        body: Dict[str, Any]
    ) -> Optional[Sequence[Union[Dict[str, Any], Block]]]:
        """
        Processes a Slack event and returns a response in the form of message blocks.

        Args:
            body (Dict[str, Any]): The body of the Slack event. Contains details about
                                the Slack event, including message text and user information.
        Returns:
            Optional[Sequence[Union[Dict[str, Any], Block]]]: A sequence of response blocks or None.
        """
        # Response blocks
        blocks: Optional[Sequence[Union[Dict[str, Any], Block]]] = []

        # Get the text from the event
        text = body.get("event", {}).get("text", "")

        if text is not None and "wake up" in text:
            user = body.get("event", {}).get("user", "")
            response_message = f"Hi <@{user}>! How are you feeling!"

            # Create a response
            blocks.append(SectionBlock(block_id="response", text=response_message))

            # Add buttons to the response
            blocks.append(
                ActionsBlock(
                    block_id="how_are_you",
                    elements=[
                        ButtonElement(
                            action_id="good",
                            text=TextObject(type=PlainTextObject.type, text="Good", emoji=True),
                            value="good",
                            style="primary",
                        ),
                        ButtonElement(
                            action_id="bad",
                            text=TextObject(type=PlainTextObject.type, text="Bad", emoji=True),
                            value="bad",
                            style="danger",
                        ),
                    ],
                )
            )
        else:
            blocks.append(
                SectionBlock(
                    block_id="response", text=MarkdownTextObject(text="*Sleeeeeping* :sleeping:")
                )
            )

        return blocks

    @staticmethod
    async def get_quote(search_index: str) -> Optional[Tuple[str, str]]:
        """
        Retrieves a random quote from a Redis database using the provided search index.

        Connects to a Redis database, performs a search for all entries, and selects one
        randomly. Returns the selected quote along with the author's name.

        Args:
            search_index (str): The name of the Redis search index to use for querying quotes.

        Returns:
            Optional[Tuple[str, str]]: A tuple containing the quote and the author's name,
                                    or None if no quote is found.
        """
        redis_search_dao = AsyncRedisDAOFactory.create_redis_dao_with_existing_pool(
            search_index_name=search_index
        )

        query = Query("*").verbatim().no_content().paging(0, 0)
        results = await redis_search_dao.index_search(query)
        total_entries = results["total_results"]

        logger.info("Results count:%s", total_entries)

        entry = None

        if total_entries > 0:
            # Generate a random offset
            random_offset = random.randint(0, total_entries - 1)

            # Retrieve the entry at the random offset
            query = Query("*").verbatim().paging(random_offset, 1)
            random_entry_query = await redis_search_dao.index_search(query)

            logger.info("Results random: %s", random_entry_query)
            attributes = random_entry_query["results"][0]["extra_attributes"]
            entry = (attributes["quote"], attributes["person"])

        return entry

    @staticmethod
    async def handle_good_interaction(
        search_index: str,
    ) -> Optional[Sequence[Union[Dict[str, Any], Block]]]:
        """
        Generates a response for a 'good' interaction in Slack, potentially including a random quote.

        If the user interaction is positive ('good'), this method fetches a random quote and
        forms a response including the quote. If no quote is available, a generic positive
        response is returned.

        Args:
            search_index (str): The name of the Redis search index to use for querying quotes.

        Returns:
            Optional[Sequence[Union[Dict[str, Any], Block]]]: A sequence of message blocks
                                                            to be sent as a response in Slack,
                                                            or None if no response is needed.
        """

        # Response blocks
        blocks: Optional[Sequence[Union[Dict[str, Any], Block]]] = []

        random_quote = await SlackService.get_quote(search_index)

        if random_quote:
            blocks.append(
                SectionBlock(
                    block_id="response_1",
                    text=MarkdownTextObject(
                        text="*Amazing!* Let's see if this quote will enhance your day a bit more."
                    ),
                )
            )
            blocks.append(
                SectionBlock(
                    block_id="response_2",
                    text=MarkdownTextObject(text=f'*"{random_quote[0]}"* by {random_quote[1]}'),
                )
            )
        else:
            blocks.append(
                SectionBlock(block_id="response", text=MarkdownTextObject(text="*As you were!*"))
            )

        return blocks

    @staticmethod
    async def handle_bad_interaction(
        search_index: str,
    ) -> Optional[Sequence[Union[Dict[str, Any], Block]]]:
        """
        Generates a response for a 'bad' interaction in Slack, potentially including a random quote.

        If the user interaction is negative ('bad'), this method fetches a random quote and
        forms an encouraging response including the quote. If no quote is available, a generic
        comforting response is returned.

        Args:
            search_index (str): The name of the Redis search index to use for querying quotes.

        Returns:
            Optional[Sequence[Union[Dict[str, Any], Block]]]: A sequence of message blocks
                                                            to be sent as a response in Slack,
                                                            or None if no response is needed.
        """
        # Response blocks
        blocks: Optional[Sequence[Union[Dict[str, Any], Block]]] = []

        random_quote = await SlackService.get_quote(search_index)

        if random_quote:
            blocks.append(
                SectionBlock(
                    block_id="response_1",
                    text=MarkdownTextObject(
                        text="Let's see if the universe has something good to say."
                    ),
                )
            )
            blocks.append(
                SectionBlock(
                    block_id="response_2",
                    text=MarkdownTextObject(text=f'*"{random_quote[0]}"* by {random_quote[1]}'),
                )
            )
        else:
            blocks.append(
                SectionBlock(
                    block_id="response",
                    text=MarkdownTextObject(text="*I'd hope things will get better soon.*"),
                )
            )

        return blocks
