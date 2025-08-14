from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams

# Adjust the URL to your deployed MCP server
MCP_SERVER_URL = "https://hello-world-mcp-server-207195257545.europe-west1.run.app/mcp"

root_agent = Agent(
    name="helloworld_agent",
    model="gemini-2.0-flash",
    description="An agent to greet the user and add two numbers.",
    instruction="You're a simple agent that greets the user and adds two numbers using the tools provided.",
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=MCP_SERVER_URL,
            ),
        )
    ],
)