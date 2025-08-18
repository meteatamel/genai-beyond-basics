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

> [!NOTE]
> 
> The MCP Python SDK used in the code samples on https://modelcontextprotocol.io uses outdated `FastMCP 1.0`.
> Instead, you should use `FastMCP 2.0` from here: https://gofastmcp.com/. You can tell if you're using the right one in the code as follows:
> 
> `from mcp.server import FastMCP` ==> This is FastMCP 1.0: DO NOT USE
> 
> `from fastmcp import FastMCP` ==> This is FastMCP 2.0: USE THIS ONE
