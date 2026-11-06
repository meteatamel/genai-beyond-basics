# A2UI Express & Swappable Inference Formats Explorer

An interactive side-by-side web application using the official [A2UI Python Agent SDK](https://pypi.org/project/a2ui-agent-sdk/) (`a2ui-agent-sdk`), `google-genai`, and the official [`@a2ui/lit`](https://www.npmjs.com/package/@a2ui/lit) v0.9 Web Component renderer to demonstrate **Swappable Inference Formats** in A2UI.

## Overview

Standard JSON (`createSurface`, `updateComponents`, `updateDataModel`) is an ideal wire protocol for client renderers (Lit, React, Angular, Flutter), but having an LLM generate deeply nested wire JSON directly (`DirectJsonFormatFactory`) is verbose, token-heavy, and slow.

A2UI decouples the **inference format** (what the LLM writes) from the **wire format** (the standard A2UI JSON that renderers consume):

```text
[1. Python Agent SDK (a2ui-agent-sdk)]
       ↓ processor.prompt_snippet
[2. What the LLM Generates (<a2ui-json> or <a2ui> DSL)]
       ↓ processor.parse_response() compiles DSL to Wire JSON
[3. What the Renderer Gets (Validated A2UI v0.9 Wire JSON)]
       ↓ MessageProcessor + <a2ui-surface>
[4. Rendered UI (@a2ui/lit v0.9)]
```

Using [`app.py`](./app.py), you can compare **Direct JSON** (`DirectJsonFormatFactory`) side-by-side against all 3 alternative inference formats in `a2ui-agent-sdk`:

1. **A2UI Express (`ExpressFormatFactory`, Default)**: Python-like positional DSL (`root = Card(main_col)`, `_` for omitted optional args, `$/path = value` for data bindings, `?required(...)` for validation checks). Cuts system prompt size by **~55%**, reduces output tokens by **~3.5x–5.5x**, and runs accurately even with `thinking_budget=0`.
2. **Atom (`AtomFormatFactory`, Experimental)**: Lisp S-expression DSL (`(Card (Column :id "main_col" ...))`).
3. **Elemental (`ElementalFormatFactory`, Experimental)**: HTML Custom Elements DSL (`<ui-card id="root"><ui-column id="main_col">...`).

### Features

* **4-Step Pipeline Visualization**: Each column displays (1) the Python `a2ui-agent-sdk` code, (2) raw LLM inference output, (3) validated A2UI v0.9 wire JSON sent to the renderer, and (4) the live rendered `<a2ui-surface>`.
* **3 Instant UI Presets (no API key required)**:
  * **Restaurant Reservation Form**: Guest details, party size, time, dietary notes, and Confirm/Cancel actions.
  * **Login Form with Validation**: Email & password client-side validation rules (`?required`, `?email`, `?length`, `?and`).
  * **Notification Permission Card**: The exact card featured in the [Google Developers A2UI Express blog post](https://developers.googleblog.com/fast-reliable-a2ui/).
* **Live Gemini Mode (`gemini-2.5-flash`, `thinking_budget=0`)**: Enter any custom UI prompt and call Gemini live to compare real input tokens, output tokens, and end-to-end inference latency across formats.

## Run the Explorer

### Option 1: Run directly with `uv`

```sh
# Optional: set GEMINI_API_KEY (or create a local .env file from .env.example)
# to enable Live Gemini generation in the UI
export GEMINI_API_KEY="your_gemini_api_key_here"

uv run --with a2ui-agent-sdk --with google-genai --with fastapi --with uvicorn python app.py
```

Then open **http://127.0.0.1:8080** in your browser.

### Option 2: Run with `venv` and `pip`

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Running the Restaurant Finder App with A2UI Express

You can also run the full Restaurant Finder sample in the [google/A2UI](https://github.com/google/A2UI) repository using A2UI Express (`A2UI_FORMAT=express`) with the Lit client renderer:

1. Clone and install the `google/A2UI` workspace:

   ```sh
   git clone https://github.com/google/a2ui.git
   cd a2ui
   corepack enable
   PUPPETEER_SKIP_DOWNLOAD=true yarn install
   ```

2. In **Terminal 1**, start the Restaurant Finder agent with `A2UI_FORMAT=express`:

   ```sh
   # With a live Gemini model:
   GEMINI_API_KEY="your_gemini_api_key_here" A2UI_FORMAT=express \
     yarn workspace @a2ui/agent-restaurant-node run start

   # Or without an API key (canned stub mode):
   STUB_LLM=true A2UI_FORMAT=express \
     yarn workspace @a2ui/agent-restaurant-node run start
   ```

3. In **Terminal 2**, build the Lit renderer and start the shell client:

   ```sh
   cd samples/client/lit
   yarn build:renderer && yarn serve:shell
   ```

4. Open `http://localhost:5173/?app=restaurant` and prompt the agent (e.g., `Top 5 Chinese restaurants in New York`).

## References

* [Blog: Fast, reliable A2UI, with swappable inference formats](https://developers.googleblog.com/fast-reliable-a2ui/)
* [Docs: Swappable Inference Formats](https://a2ui.org/concepts/inference-formats/)
* [Spec: A2UI Express Technical Specification](https://github.com/google/A2UI/blob/main/specification/proposals/express/a2ui_express.md)
* [PyPI: `a2ui-agent-sdk`](https://pypi.org/project/a2ui-agent-sdk/)
* [npm: `@a2ui/agent`](https://www.npmjs.com/package/@a2ui/agent)
