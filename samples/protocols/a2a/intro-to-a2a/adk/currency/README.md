# Currency Agent - A2A

A currency conversion agent that uses Agent Development Kit (ADK) and exposed as an A2A server.

## Start the agent with the A2A server

Create and activate a virtual environment:

```shell
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

Set environment variables for your project:

```shell
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=genai-atamel
export GOOGLE_CLOUD_LOCATION=us-central1
```

Run the A2A agent server locally:

```shell
uvicorn agent:a2a_app --host localhost --port 8001
```

## Test the A2A server

Check that the Agent Card is published at [`http://localhost:8001/.well-known/agent-card.json`](http://localhost:8001/.well-known/agent-card.json)

You can also use [A2A Inspector](https://github.com/a2aproject/a2a-inspector).

## Deploy to Cloud Run

Change [agent.py](./agent.py) to point to a Cloud Run instance:

```python
# a2a_app = to_a2a(root_agent, port=int(os.getenv('PORT', '8001')))
a2a_app = to_a2a(root_agent, host="a2a-currency-agent-207195257545.us-central1.run.app", port=int(os.getenv('PORT', '8001')))
```

Deploy to Cloud Run:

```shell
gcloud run deploy a2a-currency-agent \
    --port=8080 \
    --source=. \
    --allow-unauthenticated \
    --region="us-central1" \
    --project="genai-atamel" \
    --set-env-vars=GOOGLE_CLOUD_PROJECT="genai-atamel",GOOGLE_CLOUD_REGION="us-central1",GOOGLE_GENAI_USE_VERTEXAI="true"
```

Check that the Agent Card is published at [`https://a2a-currency-agent-207195257545.us-central1.run.app/.well-known/agent-card.json`](https://a2a-currency-agent-207195257545.us-central1.run.app/.well-known/agent-card.json)

> [!WARNING]
> Deployment of currency agent to Cloud Run works but the travel helper agent cannot use it. I think it is due to this
> bug: [2405](https://github.com/google/adk-python/issues/2405)
