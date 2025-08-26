from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
import google.auth.transport.requests
import google.oauth2.id_token

# Adjust the URL to your deployed MCP server
MCP_SERVER_URL = "https://hello-world-mcp-server-auth-207195257545.europe-west1.run.app"


def get_id_token(audience: str) -> str:
    """
    Generates a Google Cloud Identity Token.

    Args:
        audience: The intended audience for the token (e.g., a service URL).

    Returns:
        The identity token as a string.
    """
    auth_req = google.auth.transport.requests.Request()
    credentials = google.oauth2.id_token.fetch_id_token_credentials(audience, auth_req)
    credentials.refresh(auth_req)

    id_token = credentials.token
    return id_token


id_token = get_id_token(f"{MCP_SERVER_URL}/")

root_agent = Agent(
    name="helloworld_agent",
    model="gemini-2.0-flash",
    description="An agent to greet the user and add two numbers.",
    instruction="You're a simple agent that greets the user and adds two numbers using the tools provided.",
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                headers={
                    "Authorization": f"Bearer {id_token}"
                },
                url=f"{MCP_SERVER_URL}/mcp",
            ),
        )
    ],
)