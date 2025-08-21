# Travel Helper Agent

Travel helper is an ADK agent using a local weather agent and a remote currency agent.

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

> [!WARNING]
> Make sure the currency agent is running locally or on Cloud Run before starting the travel helper agent.

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

Ask a question for the remote agent:

```shell
[user]: How much is 1 GBP in EUR?

[travel_helper_agent]: 1 British Pounds (GBP) = 1.1567 Euros (EUR)
```
