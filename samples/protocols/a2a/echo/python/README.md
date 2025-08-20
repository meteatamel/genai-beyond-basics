# Echo Agent - Python

A simple echo agent that demonstrates the core concepts of A2A protocol. This agent receives messages and respond by echoing them back, providing a clear example of how A2A communication flows.

Create and activate a virtual environment:

```shell
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```shell
pip install -r requirements.txt
```

Start the agent:

```shell
python __main__.py

INFO:     Started server process [61536]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5209 (Press CTRL+C to quit)
```

In a separate terminal, test the agent:

```shell
python a2a_client.py

INFO:httpx:HTTP Request: POST http://localhost:5209/agent "HTTP/1.1 200 OK"
{'id': '2a369695-7b4a-49bf-8cdb-5f4e1622da73', 'jsonrpc': '2.0', 'result': {'kind': 'message', 'messageId': 'a0654c73-60f8-43aa-ab21-68ee427d47df', 'parts': [{'kind': 'text', 'text': 'Echo: "Hello from the A2A client!"'}], 'role': 'agent'}}
```

## References

* [Python Quickstart Tutorial: Building an A2A Agent](https://a2a-protocol.org/latest/tutorials/python/1-introduction/)
* [A2A Python SDK](https://github.com/a2aproject/a2a-python)