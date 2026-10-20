# A2A CLI

[A2A CLI](https://github.com/a2aproject/a2a-cli) (`a2a`) is the official command-line interface for discovering, messaging, and managing [A2A (Agent2Agent)](https://a2a-protocol.org/latest/) agents from your terminal.

In addition to acting as a client for any A2A server, `a2a` includes a built-in **server mode** (`a2a server`) that can run an echo server, wrap any script or command as an A2A agent, or proxy A2A traffic.

## Install A2A CLI

Install via Homebrew (macOS / Linux):

```shell
brew tap a2aproject/a2a-cli https://github.com/a2aproject/a2a-cli
brew install a2a
```

Or install from source with Go:

```shell
go install github.com/a2aproject/a2a-cli@latest
mv "$(command -v a2a-cli)" "$(dirname "$(command -v a2a-cli)")/a2a"
```

Verify the installation:

```shell
a2a --version
```

## 1. Test the Python Echo Agent (`a2a card get` & `a2a send`)

First, start the [Python Echo Agent](../echo-agent/python/) server in one terminal:

```shell
cd ../echo-agent/python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python __main__.py

INFO:     Started server process [13641]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:5209 (Press CTRL+C to quit)
```

In a separate terminal, use `a2a` to discover the agent card and send a message:

```shell
# Discover the agent card
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

```shell
# Send a message to the agent
a2a send -a http://localhost:5209 "Hello from the A2A CLI"

[agent] Echo: Hello from the A2A CLI
```

## 2. Zero-Code Echo Server (`--echo`)

You can also start a compliant A2A Echo Agent server directly from your terminal without writing any Python or C# code:

```shell
a2a server --echo --port 8080 --name "Echo Agent" --description "An agent that echoes messages back."
```

In a separate terminal, discover the agent card and send a message:

```shell
# Fetch the agent card
a2a card get http://localhost:8080

Name:         Echo Agent
Description:  An agent that echoes messages back.
Version:      1.0.0
Interfaces:
  HTTP+JSON    http://127.0.0.1:8080
Streaming:    true
```

```shell
# Send a message
a2a send -a http://localhost:8080 "Hello from A2A CLI"

Task:     01a154bc-0736-7274-bbe7-b5cf583439b5
Context:  01a154bc-0736-735f-a194-9560779880ea
Status:   completed (2026-10-19T16:16:11+01:00)
Artifacts:
  [01a154bc-0736-7451-b3c7-6c65766b2b19] Hello from A2A CLI
History:
  [user] Hello from A2A CLI
```

## 3. Turn Any Script into an A2A Agent (`--exec`)

With `--exec`, `a2a server` runs any subprocess or script as an A2A agent. Incoming message text is passed to `stdin`, and `stdout` is returned as the task artifact. The script does not need any A2A SDK dependencies.

See [`word_processor.py`](./word_processor.py), a plain Python script that reads text from `stdin` and outputs each word in uppercase with a short delay.

Start the A2A server wrapping `word_processor.py`:

```shell
a2a server --exec "python3 -u word_processor.py" \
  --port 8080 \
  --name "Word Processor Agent" \
  --description "Converts words to uppercase."
```

Send a message to the agent:

```shell
a2a send -a http://localhost:8080 "hello agent world"

Task:     01a154c9-b728-71b9-b242-191c2ce3e56e
Context:  01a154c9-b728-77db-82df-a175c0b36fd0
Status:   completed (2026-10-19T16:31:09+01:00)
Artifacts:
  [01a154c9-bb12-7ad5-8836-e79fedcbb279] [1/3] HELLO
[2/3] AGENT
[3/3] WORLD

History:
  [user] hello agent world
```

### Streaming Chunks (`--chunk`)

Add `--chunk` on the server to split `stdout` on a delimiter and stream each piece as an A2A `ArtifactUpdateEvent` in real time:

```shell
a2a server --exec "python3 -u word_processor.py" \
  --chunk=$'\n' \
  --port 8080 \
  --name "Word Processor Agent" \
  --description "Streams words in uppercase."
```

Pass `--stream` on the client to watch task events arrive live:

```shell
a2a send -a http://localhost:8080 --stream "hello agent world"

Task:     01a154c9-bf34-7bb0-b949-f632a913ca5e
Context:  01a154c9-bf34-7cb2-b457-904e4dd2ed6e
Status:   submitted
History:
  [user] hello agent world
[status] working
[artifact] [1/3] HELLO
[artifact+] [2/3] AGENT
[artifact+] [3/3] WORLD
[status] completed
```

You can also format output as JSON (`-o json`) or JSON Lines (`-o jsonl`) for shell pipelines and automation:

```shell
a2a send -a http://localhost:8080 --stream -o jsonl "hello agent world"
```

## 4. A2A Debugging Proxy (`--proxy`)

You can run `a2a server --proxy` in front of any upstream A2A agent (such as the Echo Agent or ADK Currency Agent) to log traffic, inspect requests, or inject authentication and tracing headers.

With an upstream agent running on port `8080`, start the proxy on port `9090`:

```shell
a2a server --proxy -a http://localhost:8080 --port 9090

Proxying to "Word Processor Agent" agent
Listening on 127.0.0.1:9090
```

Send requests through the proxy:

```shell
a2a send -a http://localhost:9090 "hello agent world"
```

## 5. Teach AI Coding Assistants the A2A Skill (`a2a skill`)

`a2a-cli` bundles a ready-made `SKILL.md` that teaches AI coding assistants (such as Antigravity, Gemini CLI, Claude Code, or Cursor) how to discover and delegate tasks to remote A2A agents:

```shell
a2a skill
```

## References

* [GitHub: A2A CLI](https://github.com/a2aproject/a2a-cli)
* [A2A CLI Command Reference](https://github.com/a2aproject/a2a-cli/blob/main/internal/README.md)
