# Introduction to Model Context Protocol (MCP)

MCP is an open protocol that standardizes how applications provide context to large language models (LLMs).

It has 3 distinct parts:

| Primitive    | Who controls it?                                        | Use Cases                                                  |
|:-------------|:--------------------------------------------------------|:-----------------------------------------------------------|
| **Tools**    | **Model-controlled:** Model decides when to call these  | Give additional functionality to the model                 |
| **Resources**| **App-controlled:** App decides when to call these      | Get additional data/context to messages                    |
| **Prompts**  | **User-controlled:** The user decides when to use these | Workflows to run based on user input, like a slash command |

Follow these steps to learn about MCP:

* [Use an existing MCP server](./use-existing-mcp/)
* [Create a local MCP server](./create-local-mcp/)
* [Deploy MCP server to Cloud Run](./deploy-mcp-to-cloudrun/)
* [Document MCP server with tools, resources, prompt](./document-server)

> [!NOTE]
> 
> The MCP Python SDK used in the code samples on https://modelcontextprotocol.io uses outdated `FastMCP 1.0`.
> Instead, you should use `FastMCP 2.0` from here: https://gofastmcp.com/. You can tell if you're using the right one in the code as follows:
> 
> `from mcp.server import FastMCP` ==> This is FastMCP 1.0: DO NOT USE
> 
> `from fastmcp import FastMCP` ==> This is FastMCP 2.0: USE THIS ONE
> 
> There's different levels of MCP support in various tools.
> For example:
> * **MCP inspector** supports both stdio and HTTP transport. It supports MCP tools, resources, resource templates, and prompts.
> * **Claude Desktop** supports only stdio but not HTTP transport. It supports MCP tools, resources, prompts but not resource templates.
> * **Gemini CLI** supports both stdio and HTTP transport. It supports MCP tools and prompts but not resources or resource templates.
> * **ADK** supports both stdio and HTTP transport. It supports MCP tools only.
