# Travel Helper Agent

Travel helper is an ADK agent using a local weather agent and a remote currency agent.

## Start the agent

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

## Test the agent with the currency agent on local A2A server

> [!WARNING]
> Make sure the currency agent is running locally before running the travel helper agent.

Run the agent:

```shell
adk run .

...
Running agent travel_helper_agent, type exit to exit.
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

## Test the agent with the currency agent on Cloud Run

> [!WARNING]
> Make sure the currency agent is deployed on Cloud Run before running the travel helper agent.

Change [agent.py](./agent.py) to point to a Cloud Run instance:

```python
# agent_card=f"http://localhost:8001/{AGENT_CARD_WELL_KNOWN_PATH}"
agent_card=f"https://a2a-currency-agent-207195257545.us-central1.run.app/{AGENT_CARD_WELL_KNOWN_PATH}"
```

Run the agent:

```shell
adk run .

...
Running agent travel_helper_agent, type exit to exit.
```

> [!WARNING]
> Deployment of currency agent to Cloud Run works but the travel helper agent cannot use it. I think it is due to this
> bug: [2405](https://github.com/google/adk-python/issues/2405)
