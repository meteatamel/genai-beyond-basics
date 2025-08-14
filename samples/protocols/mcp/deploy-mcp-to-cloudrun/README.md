# Deploy MCP server to Cloud Run

Let's deploy the local MCP server to Cloud Run, so others can also use the MCP server.

## Get server ready for Cloud Run

First, you need to modify the [server.py](./server.py) slightly for Cloud Run:

```python
if __name__ == "__main__":
    # host="0.0.0.0" and port are required for Cloud Run
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=os.getenv("PORT", 8080)
    )
```

Also create a [Dockerfile](./Dockerfile) to containerize the app for Cloud Run.

## Deploy to Cloud Run

```shell
gcloud run deploy hello-world-mcp-server \
    --allow-unauthenticated \
    --region europe-west1 \
    --source .
```

> [!CAUTION]
> In production, you don't want to deploy with `--allow-unauthenticated flag.`
> Instead, use `--no-allow-unauthenticated` flag and Cloud Run Proxy to authenticate.
> See [Build and deploy a remote MCP Server on Cloud Run](https://cloud.google.com/run/docs/tutorials/deploy-remote-mcp-server)

## Test with MCP inspector

In a separate terminal, start the MCP inspector:

```shell
npx @modelcontextprotocol/inspector
```

In MCP inspector, set the following:

Transport type: `Stremable HTTP`
URL: `https://hello-world-mcp-server-207195257545.europe-west1.run.app/mcp`

Now, you're talking to the MCP server running on Cloud Run over streamable HTTP.

## Test with Gemini CLI

Let's configure the MCP server on Cloud Run in [`.gemini/settings.json`](./gemini/settings.json) file:

```shell
{
  "mcpServers": {
    "helloworld": {
      "httpUrl": "https://hello-world-mcp-server-207195257545.europe-west1.run.app/mcp"
    }
  }
}
```

Now, when you start Gemini CLI, you can simply do `/mcp list` and see the filesystem server:

```shell
ℹ Configured MCP servers:

ℹ Configured MCP servers:

  🟢 helloworld - Ready (2 tools)
    Tools:
    - add
    - greet
```

You can then try the following prompt to see if Gemini CLI uses the filesystem server: `Greet Mete` or `Add 2 and 3`.
