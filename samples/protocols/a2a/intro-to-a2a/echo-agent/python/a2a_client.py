import asyncio
import httpx
import logging
from typing import Any
from uuid import uuid4


from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    MessageSendParams,
    SendMessageRequest,
    SendStreamingMessageRequest,
)
from a2a.utils.constants import (
    AGENT_CARD_WELL_KNOWN_PATH,
    PREV_AGENT_CARD_WELL_KNOWN_PATH
)

BASE_URL = 'http://localhost:5209'

async def main() -> None:
    """A2A client to test the A2A server."""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    async with httpx.AsyncClient() as httpx_client:
        # 1. Get the agent card
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL,
            # Use the legacy path if talking to C# A2AAgent
            #agent_card_path=PREV_AGENT_CARD_WELL_KNOWN_PATH
        )

        agent_card = None

        try:
            logger.info(
                f'Attempting to fetch public agent card from: {BASE_URL}'
            )
            agent_card = await resolver.get_agent_card()

            logger.info('Successfully fetched public agent card:')
            logger.info(
                agent_card.model_dump_json(indent=2, exclude_none=True)
            )
        except Exception as e:
            logger.error(
                f'Critical error fetching public agent card: {e}', exc_info=True
            )
            raise RuntimeError(
                'Failed to fetch the public agent card. Cannot continue.'
            ) from e

        # 2. Create an A2A client to communicate with the agent using url from the agent card
        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=agent_card
        )
        logger.info('A2AClient initialized.')

        # 3. Create a message to send to the agent
        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': '"Hello from the A2A client!"'}
                ],
                'messageId': uuid4().hex,
            },
        }
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(**send_message_payload)
        )

        # 4. Send the message using non-streaming API
        response = await client.send_message(request)
        print(response.model_dump(mode='json', exclude_none=True))

        # 5. Send the message using streaming API
        streaming_request = SendStreamingMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )

        stream_response = client.send_message_streaming(streaming_request)

        async for chunk in stream_response:
            print(chunk.model_dump(mode='json', exclude_none=True))


if __name__ == '__main__':
    asyncio.run(main())
