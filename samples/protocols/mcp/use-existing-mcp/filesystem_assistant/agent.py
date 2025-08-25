import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# IMPORTANT: This MUST be an ABSOLUTE path to a folder the npx process can access.
# Replace with a valid absolute path on your system.
TARGET_FOLDER_PATH = "/Users/atamel/Desktop" # On Mac
#TARGET_FOLDER_PATH = "/home/atamel/" # on Cloud Shell

instruction_prompt = f"""
    You're the file system assistant agent. Your task is to help the user to manage its files on the filesystem.
    Use the {TARGET_FOLDER_PATH} as the default folder and generate a reasonable file name if the user did not
    specify a file name. Do not ask confirmations from the user.
"""

root_agent = Agent(
    name='filesystem_assistant_agent',
    model='gemini-2.0-flash',
    description="An agent to help the user to manager their files. You can list files, read files, etc.",
    instruction=instruction_prompt,
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y",  # Argument for npx to auto-confirm install
                    "@modelcontextprotocol/server-filesystem",
                    os.path.abspath(TARGET_FOLDER_PATH),
                ],
            ),
            # Optional: Filter which tools from the MCP server are exposed
            # tool_filter=['list_directory', 'read_file']
        )
    ],
)