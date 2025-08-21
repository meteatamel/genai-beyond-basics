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

Run the A2A agent server:

```shell
uvicorn agent:a2a_app --host localhost --port 8001
```

TODO: Deploy to Cloud Run
