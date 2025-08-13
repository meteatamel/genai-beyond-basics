# Create a local MCP server

Let's build a minimal MCP server and run it locally.

## FastMCP 2.0

[FastMCP](https://gofastmcp.com/) 2.0 is the easiest way to create MCP servers and clients in Python.

Create a Python env and install FastMCP:

```shell
python -m venv .venv
source .venv/bin/activate
pip install fastmcp
```

## Server with stdio transport

See [server.py](server.py) with a minimal MCP server with 2 MCP tools.

By default, it uses the stdio transport. When using stdio transport, you will typically not run the server yourself as a separate process. Rather, your clients will spin up a new server process for each session:

```python
if __name__ == "__main__":
    # By default, it uses the stdio transport
    mcp.run()
```

You can test the server with `fastmcp`:

```shell
fastmcp run server.py:mcp
```

Or simply with `python`:

```shell
python server.py
```

You can also run via MCP inspector through `fastmcp`:

```shell
fastmcp dev server.py
```

Or directly with MCP inspector which starts the server in session:

```shell
npx @modelcontextprotocol/inspector python server.py
```

## Server with streaming HTTP transport

Switch to streaming-http transport:

```python
if __name__ == "__main__":
    # Both 'http' or 'streaming-http' refer to the same streaming-http transport
    # mcp.run(transport="http")
    mcp.run(transport="http", host="127.0.0.1", port=8000)
```

Now, you need to run the server:

```shell
python server.py
```

In a separate terminal, start the MCP inspector:

```shell
npx -y @modelcontextprotocol/inspector
```

In MCP inspector, set the following:

Transport type: `Stremable HTTP`
URL: `http://127.0.0.1:8000/mcp`

Now, you're talking to the server over streamable HTTP.
