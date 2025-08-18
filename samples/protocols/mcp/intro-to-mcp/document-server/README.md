# Document MCP server with tools, resources, prompt

See [server.py](./server.py) for a sample document MCP server that uses MCP tools, resources, and prompts to read
and edit documents and format them into markdown.

## Test with MCP inspector

Start the server:

```shell
python server.py
```

In a separate terminal, start the MCP inspector:

```shell
npx @modelcontextprotocol/inspector
```

In MCP inspector, set the following:

Transport type: `Stremable HTTP`
URL: `http://127.0.0.1:8000/mcp`

Now, you can browse Prompts, Resources, Resource Templates, and Tools.

## Test with Gemini CLI

Let's configure the MCP server on Cloud Run in [`.gemini/settings.json`](./gemini/settings.json) file:

```shell
{
  "mcpServers": {
    "documentServer": {
      "httpUrl": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Now, when you start Gemini CLI, you can simply do `/mcp list`:

```shell
ℹ Configured MCP servers:

  🟢 documentServer - Ready (2 tools, 1 prompt)
    Tools:
    - edit_document
    - read_doc_contents

    Prompts:
    - format
```

You can now try to use the prompt by typing `/format` which should prompt you for `--doc_id`. You can try formatting
one of the files:

```shell
/format --doc_id="spec.txt"
```

This should prompt for `read_doc_contents` and `edit_document` tools and in the end, you should have the `spec.txt`
formatted in markdown. 
