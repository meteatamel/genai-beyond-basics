import asyncio
import logging
import httpx

from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import (
    display_agent_card,
    get_stream_response_text,
    new_text_message,
)
from a2a.types import Role, SendMessageRequest

BASE_URL = 'http://localhost:5209'


async def main() -> None:
    """A2A client to test the A2A server."""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # 1. Get the agent card
    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL,
        )
        logger.info(f'Attempting to fetch public agent card from: {BASE_URL}')
        agent_card = await resolver.get_agent_card()
        logger.info('Successfully fetched public agent card:')
        display_agent_card(agent_card)

    # 2. Create a message to send to the agent
    message = new_text_message('Hello from the A2A client!', role=Role.ROLE_USER)
    request = SendMessageRequest(message=message)

    # 3. Send the message using non-streaming API
    print('\n=== Non-Streaming Communication ===')
    non_streaming_client = await create_client(
        agent=agent_card,
        client_config=ClientConfig(streaming=False),
    )
    async for chunk in non_streaming_client.send_message(request):
        print(f'Received response: {get_stream_response_text(chunk)}')
    await non_streaming_client.close()

    # 4. Send the message using streaming API
    print('\n=== Streaming Communication ===')
    streaming_client = await create_client(
        agent=agent_card,
        client_config=ClientConfig(streaming=True),
    )
    async for chunk in streaming_client.send_message(request):
        print(f'Received streaming chunk: {get_stream_response_text(chunk)}')
    await streaming_client.close()


if __name__ == '__main__':
    asyncio.run(main())

