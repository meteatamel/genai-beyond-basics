from a2a.helpers import get_message_text, new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from agent import EchoAgent


class EchoAgentExecutor(AgentExecutor):
    """A wrapper around the EchoAgent to implement execute and cancel methods in order to participate in A2A framework."""

    def __init__(self):
        self.agent = EchoAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = get_message_text(context.message)
        result = await self.agent.invoke(query)
        await event_queue.enqueue_event(
            new_text_message(result)
        )

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise NotImplementedError('cancel not supported')
