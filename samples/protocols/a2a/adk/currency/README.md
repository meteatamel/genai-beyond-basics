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
export GOOGLE_CLOUD_LOCATION=global
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

Check that the Agent Card is published at [`http://localhost:8080/.well-known/agent-card.json`](http://localhost:8080/.well-known/agent-card.json).

You can test the agent from your terminal using [A2A CLI](https://github.com/a2aproject/a2a-cli) (`a2a`):

```shell
# Discover the agent card
a2a card get http://localhost:8080

Name:         currency_agent
Description:  Agent to convert from one currency to another.
Version:      0.0.1
Interfaces:
  JSONRPC      http://localhost:8080
Streaming:    true
Skills:
  currency_agent       model
  currency_agent-convert_currency convert_currency
```

```shell
# Send a currency conversion question
a2a send -a http://localhost:8080 "How much is 1 GBP in EUR?"

Task:     598a1dce-f628-45cc-bbe0-305a639ffc02
Context:  8e770de5-beb6-4a48-8c43-9e0736b696bf
Status:   completed (2026-10-19T15:29:30Z)
Artifacts:
  [93ef7de9-fb90-4b19-a4e3-aadc07c057ab] 1 British Pounds (GBP) = 1.1876 Euros (EUR)
History:
  [user] How much is 1 GBP in EUR?
  [agent] {"args":{"from_currency":"GBP","to_currency":"EUR"},"id":"call_2821308","name":"convert_currency"}
  [agent] {"id":"call_2821308","name":"convert_currency","response":{"result":1.1876}}
  [agent] 1 British Pounds (GBP) = 1.1876 Euros (EUR)
```

You can also use [A2A Inspector](https://github.com/a2aproject/a2a-inspector).

## Deploy to Cloud Run

Change [agent.py](./agent.py) to point to a Cloud Run instance:

```python
# Expose the agent over A2A protocol locally
# a2a_app = to_a2a(root_agent, host="localhost", port=int(os.getenv("PORT", "8080")))

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
