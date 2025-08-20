import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_executor import EchoAgentExecutor

PORT = 5209
BASE_URL = f'http://localhost:{PORT}'

# The entry point of the A2A server which defines the agent card and request handler and runs the server.
if __name__ == '__main__':
    # Define the agent card with the skill and capabilities
    skill = AgentSkill(
        id='echo',
        name='Echo tool',
        description='Echos every received message back to the user.',
        tags=['echo'],
        examples=['hello', 'how are you'],
    )

    agent_card = AgentCard(
        name='Echo Agent',
        description='An agent that will echo every message it receives.',
        url=BASE_URL,
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill]
    )

    # Define the request handler with the EchoAgentExecutor
    request_handler = DefaultRequestHandler(
        agent_executor=EchoAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # Create the A2A server application with the agent card and request handler
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    # Run the server
    uvicorn.run(server.build(), host='0.0.0.0', port=PORT)
