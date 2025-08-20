from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message
from agent import EchoAgent


class EchoAgentExecutor(AgentExecutor):
    """Echo Agent Executor."""

    def __init__(self):
        self.agent = EchoAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        text_message = context.message.parts[0].root.text
        result = await self.agent.invoke(text_message)
        await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise Exception('cancel not supported')

