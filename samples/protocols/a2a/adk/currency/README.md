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
uvicorn agent:a2a_app --host localhost --port 8080
```

You can also run in a container.

Build the container:

```shell
docker build -t currency-agent:0.1 .
```

Run the container:

```shell
docker run \
    -e GOOGLE_GENAI_USE_VERTEXAI=TRUE \
    -e GOOGLE_CLOUD_PROJECT=genai-atamel \
    -e GOOGLE_CLOUD_LOCATION=us-central1 \
    -p 8080:8080 currency-agent:0.1
```

## Test the A2A server

Check that the Agent Card is published at [`http://localhost:8080/.well-known/agent-card.json`](http://localhost:8001/.well-known/agent-card.json)

You can also use [A2A Inspector](https://github.com/a2aproject/a2a-inspector).

## Deploy to Cloud Run

Change [agent.py](./agent.py) to point to a Cloud Run instance:

```python
# Expose the agent over A2A protocol locally
# a2a_app = to_a2a(root_agent,
#                  host="0.0.0.0",
#                  port=int(os.getenv('PORT', '8080'))
                #  )

# Expose the agent over A2A protocol on Cloud Run
a2a_app = to_a2a(root_agent,
                 host="a2a-currency-agent-207195257545.us-central1.run.app",
                 port=443,
                 protocol="https")
```

Deploy to Cloud Run:

```shell
gcloud run deploy a2a-currency-agent \
    --port=8080 \
    --source=. \
    --allow-unauthenticated \
    --region="us-central1" \
    --project="genai-atamel" \
    --set-env-vars=GOOGLE_CLOUD_PROJECT="genai-atamel",GOOGLE_CLOUD_LOCATION="us-central1",GOOGLE_GENAI_USE_VERTEXAI="true"
```

Check that the Agent Card is published at [`https://a2a-currency-agent-207195257545.us-central1.run.app/.well-known/agent-card.json`](https://a2a-currency-agent-207195257545.us-central1.run.app/.well-known/agent-card.json)
