# Travel Helper Agent

Travel helper is an ADK agent using a local weather agent and a remote currency agent.

## Setup the travel helper agent

Create and activate a virtual environment:

```shell
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

Rename `dotenv` to `.env` and update with your API keys or projects.

## Test the local travel helper agent with the currency agent on local A2A server

> [!WARNING]
> Make sure the currency agent is running locally before running the travel helper agent.

Run the agent:

```shell
adk web
```

Ask a question for the local agent:

```shell
[user]: How's the weather in London?

[travel_helper_agent]: OK. For the next 7 days, the weather in London will be:
* Temperature: Min temperatures between 13-16°C and max temperatures between 19-24°C.
* Rain: There is a chance of rain on August 26th and 27th.
* Wind: Max wind speeds between 8-17 km/h.
* UV index: Max UV index between 4-6.
```

Ask a question for the currency agent:

```shell
[user]: How much is 1 GBP in EUR?

[travel_helper_agent]: 1 British Pounds (GBP) = 1.1567 Euros (EUR)
```

## Test the local travel helper agent with the currency agent on Cloud Run

> [!WARNING]
> Make sure the currency agent is deployed on Cloud Run before running the travel helper agent.

Change [agent.py](./agent.py) to point to a Cloud Run instance:

```python
# agent_card=f"http://localhost:8001/{AGENT_CARD_WELL_KNOWN_PATH}"
agent_card=f"https://a2a-currency-agent-207195257545.us-central1.run.app/{AGENT_CARD_WELL_KNOWN_PATH}"
```

You can now test the agent locally with `adk web` and see that it has access to currency agent deployed on Cloud Run
via A2A.

## Test the travel agent on Cloud Run with the currency agent on Cloud Run

You can also deploy the travel agent to Cloud Run. Enable the necessary services for Cloud Run:

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
  --service_name=travel-helper-agent \
  --with_ui \
  ./travel_helper
```

In this case, both the travel agent and the currency agent are deployed and managed by Cloud Run and communicating
via A2A.

> [!WARNING]
> Travel agent deployment does not seem to work due to the default `Dockerfile` not including the A2A package.
