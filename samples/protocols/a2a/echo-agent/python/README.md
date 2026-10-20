# Echo Agent - Python

A barebones agent that demonstrates the core concepts of A2A protocol. This agent receives messages and respond by
echoing them back, providing a clear example of how A2A communication flows.

![A2A Agent](../images/a2a-agent.png)

Here are the relevant files:

* [`agent.py`](./agent.py): An agent that simply echoes back the received message.
* [`agent_executor.py`](./agent_executor.py): A wrapper around the EchoAgent to implement execute and cancel methods in
order to participate in A2A framework.
* [`__main__.py`](./__main__.py): The entry point of the A2A server which defines the agent card and request handler and runs the server.
* [`a2a_client.py`](./a2a_client.py): A2A client to test the A2A server.

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

Start the A2A server with the agent:

```shell
python __main__.py

INFO:     Started server process [61536]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5209 (Press CTRL+C to quit)
```

## Test the A2A server with A2A client

In a separate terminal, test the agent:

```shell
python a2a_client.py

=== Non-Streaming Communication ===
Received response: Echo: Hello from the A2A client!

=== Streaming Communication ===
Received streaming chunk: Echo: Hello from the A2A client!
```

## Test the A2A server with A2A CLI

[A2A CLI](https://github.com/a2aproject/a2a-cli) (`a2a`) is the official command-line client for discovering and messaging A2A agents from your terminal.

Install the CLI (macOS/Linux via Homebrew):

```shell
brew tap a2aproject/a2a-cli https://github.com/a2aproject/a2a-cli
brew install a2a
```

Discover the agent card:

```shell
a2a card get http://localhost:5209

Name:         Echo Agent
Description:  An agent that will echo every message it receives.
Version:      1.0.0
Interfaces:
  JSONRPC      http://localhost:5209
Streaming:    true
Skills:
  echo                 Echo tool
```

Send a message to the agent:

```shell
a2a send -a http://localhost:5209 "Hello from the A2A CLI"

[agent] Echo: Hello from the A2A CLI
```

## Test the A2A server with A2A Inspector

[A2A Inspector](https://github.com/a2aproject/a2a-inspector) is a web-based tool designed to help developers inspect,
debug, and validate servers that implement the A2A protocol.

Follow [Setup and Running the Application](https://github.com/a2aproject/a2a-inspector?tab=readme-ov-file#setup-and-running-the-application) to install the A2A Inspector.

Inside `a2a-inspector` folder, start the A2A Inspector:

```shell
/run.sh

Starting A2A Inspector...
Starting frontend build (watch mode)...
...
[BACKEND] INFO:     Uvicorn running on http://127.0.0.1:5001 (Press CTRL+C to quit)
```

Open `http://127.0.0.1:5001` in the browser, enter `http://0.0.0.0:5209` for the agent. Now, you can connect to the
agent, download agent card, and chat with the agent over A2A:

![A2A Inspector](../images/a2a-inspector.png)

## References

* [Python Quickstart Tutorial: Building an A2A Agent](https://a2a-protocol.org/latest/tutorials/python/1-introduction/)
* [A2A Python SDK](https://github.com/a2aproject/a2a-python)
* [A2A CLI](https://github.com/a2aproject/a2a-cli)
* [A2A Inspector](https://github.com/a2aproject/a2a-inspector)
