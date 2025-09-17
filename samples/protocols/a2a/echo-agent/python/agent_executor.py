from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
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
        query = context.get_user_input()
        result = await self.agent.invoke(query)
        await event_queue.enqueue_event(
            new_agent_text_message(result)
        )

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

