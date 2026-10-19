import uvicorn
from starlette.applications import Starlette

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
)
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
)
from agent_executor import EchoAgentExecutor

PORT = 5209
BASE_URL = f'http://localhost:{PORT}'

# The entry point of the A2A server for the agent which defines the agent card and request handler and runs the server.
if __name__ == '__main__':
    # Define the agent card with the skill and capabilities
    capabilities = AgentCapabilities(
        streaming=True
    )

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
        supported_interfaces=[
            AgentInterface(
                protocol_binding='JSONRPC',
                url=BASE_URL,
                protocol_version='1.0',
            )
        ],
        version='1.0.0',
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        capabilities=capabilities,
        skills=[skill],
    )

    # Define the request handler with the EchoAgentExecutor and agent card
    request_handler = DefaultRequestHandler(
        agent_executor=EchoAgentExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=agent_card,
    )

    # Create the Starlette application with the agent card and JSON-RPC routes
    routes = []
    routes.extend(create_agent_card_routes(agent_card))
    routes.extend(create_jsonrpc_routes(request_handler, '/'))
    app = Starlette(routes=routes)

    # Run the server
    uvicorn.run(app, host='0.0.0.0', port=PORT)

