# Currency Agent - A2A

A currency conversion agent that uses Agent Development Kit (ADK) and exposed as an A2A server.

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

Check that the Agent Card is published at [`http://localhost:8001/.well-known/agent.json`](http://localhost:8001/.well-known/agent.json)

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

Check that the Agent Card is published at [`https://a2a-currency-agent-207195257545.us-central1.run.app/.well-known/agent.json`](https://a2a-currency-agent-207195257545.us-central1.run.app/.well-known/agent.json)
