# Deploy MCP server to Cloud Run

Let's deploy the local MCP server to Cloud Run, so others can also use the MCP server.

## Get MCP server ready for Cloud Run

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

## Deploy MCP server to Cloud Run (unauthenticated)

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

- Transport type: `Stremable HTTP`
- URL: `https://hello-world-mcp-server-207195257545.europe-west1.run.app/mcp`

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

Now, when you start Gemini CLI, you can simply do `/mcp list`:

```shell
ℹ Configured MCP servers:

ℹ Configured MCP servers:

  🟢 helloworld - Ready (2 tools)
    Tools:
    - add
    - greet
```

You can then try the following prompt to see if Gemini CLI uses the MCP server: `Greet Mete` or `Add 2 and 3`.

## Test with Agent Development Kit (ADK)

[ADK](https://google.github.io/adk-docs/) is an agent framework from Google. Let's see how ADK can use an MCP server
deployed on Cloud Run.

Take a look at [hello_world_agent](./hello_world_agent/). It's a minimal agent configured with the MCP server deployed
to Cloud Run. Adjust the `MCP_SERVER_URL` in the [agent.py](./hello_world_agent/agent.py) and also rename `dotenv`
to `.env` and update with your API keys or projects.

Create a Python env and install ADK:

```shell
cd hello_world_agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You can now test the agent locally with `adk web` and see that it has access to `greet` and `add` from the MCP server.

You can also deploy the agent to Cloud Run. Enable the necessary services for Cloud Run:

```shell
gcloud services enable artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com
```

Deploy using the adk tool:

```shell
adk deploy cloud_run \
  --project=genai-atamel \
  --region=us-central1 \
  --service_name=hello-world-agent \
  --with_ui \
  ./hello_world_agent
```

In this case, both the agent and the MCP server are deployed and managed by Cloud Run.

## Deploy MCP server to Cloud Run (authenticated)

Let's now deploy the same MCP server a Cloud Run service that requires authentication:

```shell
gcloud run deploy hello-world-mcp-server-auth \
    --no-allow-unauthenticated \
    --region europe-west1 \
    --source .
```

## Test with MCP inspector

First, make sure your user account has the `run.invoker` role:

```shell
PROJECT_ID=genai-atamel
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=user:$(gcloud config get-value account) \
    --role='roles/run.invoker'
```

Print the identity token for authentication:

```shell
gcloud auth print-identity-token
```

In a separate terminal, start the MCP inspector:

```shell
npx @modelcontextprotocol/inspector
```

In MCP inspector, set the following:

- Transport type: `Stremable HTTP`
- URL: `https://hello-world-mcp-server-auth-207195257545.europe-west1.run.app/mcp`
- Authentication
    - API Token Authentication
        - Header Name: Authorization
        - Bearer Token: paste_your_identity_token_here

Now, you're talking to the MCP server running on authenticated Cloud Run over streamable HTTP.

## Test with Gemini CLI

Let's configure the MCP server on Cloud Run in [`.gemini/settings.json`](./gemini/settings.json) file:

```shell
{
  "mcpServers": {
    # "helloworld": {
    #   "httpUrl": "https://hello-world-mcp-server-207195257545.europe-west1.run.app/mcp"
    # },
    "helloworld-auth": {
      "httpUrl": "https://hello-world-mcp-server-auth-207195257545.europe-west1.run.app/mcp",
      "headers": {
        "Authorization": "Bearer your-auth-token-here"
      }
    }
  }
}
```

You can then try the following prompt to see if Gemini CLI uses the MCP server: `Greet Mete` or `Add 2 and 3`.

## Test with Agent Development Kit (ADK)

Take a look at [hello_world_agent_auth](./hello_world_agent_auth/). It's a minimal agent configured with the MCP server
deployed to Cloud Run with authentication.

Adjust the `MCP_SERVER_URL` in the [agent.py](./hello_world_agent_auth/agent.py) and also rename `dotenv`
to `.env` and update with your API keys or projects.

Create a Python env and install ADK:

```shell
cd hello_world_agent_auth
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

By default, Cloud Run services run as the Compute Engine default service account (`PROJECT_NUMBER-compute@developer.gserviceaccount.com`).
Grant it with the Cloud Run Invoker Role:

```shell
gcloud run services add-iam-policy-binding hello-world-mcp-server-auth \
    --member=serviceAccount:207195257545-compute@developer.gserviceaccount.com \
    --role=roles/run.invoker \
    --region=europe-west1
```

> [!WARNING]
> In production environments, you should create a dedicated service account for the Cloud Run service instead of using
> the default Compute Engine service account.

Deploy using the adk tool:

```shell
adk deploy cloud_run \
  --project=genai-atamel \
  --region=us-central1 \
  --service_name=hello-world-agent-auth \
  --with_ui \
  ./hello_world_agent_auth
```

In this case, both the agent and the MCP server are deployed and managed by Cloud Run with authentication enabled.
