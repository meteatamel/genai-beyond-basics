#!/usr/bin/env python3
"""Interactive Side-by-Side Web UI comparing A2UI Swappable Inference Formats.

Compares:
  1. Direct JSON (DirectJsonFormatFactory)       — <a2ui-json>
  2. A2UI Express (ExpressFormatFactory, Default) — <a2ui> Python-like DSL
  3. Atom (AtomFormatFactory, Experimental)       — <a2ui> Lisp S-expressions
  4. Elemental (ElementalFormatFactory, Exp.)     — <a2ui> HTML Custom Elements

Run with:
    uv run --with a2ui-agent-sdk --with google-genai --with fastapi --with uvicorn python app.py
Then open http://127.0.0.1:8080 in your browser.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import time
import warnings

from a2ui.core.basic_catalog import BasicCatalog
from a2ui.core.schema import ProtocolVersion
from a2ui.inference_formats import (
    DirectJsonFormatFactory,
    ExpressFormatFactory,
    to_message_dicts,
)
from a2ui.inference_formats.experimental.atom import AtomFormatFactory
from a2ui.inference_formats.experimental.elemental import ElementalFormatFactory
from a2ui.parser import A2uiPart
from a2ui.processor import A2uiGenerator, CatalogConfig
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

warnings.filterwarnings("ignore", message=r"\[EXPERIMENTAL\]")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Automatically load local .env file if present
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

# ---------------------------------------------------------------------------
# Presets: Each preset is authored in compact A2UI Express (<a2ui>) and
# automatically compiled to canonical Wire JSON and decompiled into Atom and
# Elemental formats at startup.
# ---------------------------------------------------------------------------

PRESETS = {
    "reservation_form": {
        "id": "reservation_form",
        "title": "Restaurant Reservation Form",
        "description": "Interactive reservation form with guest details, party size, dietary notes, and Confirm/Cancel actions.",
        "prompt": (
            "Create a restaurant reservation form card on surface 'booking' for "
            "Xi'an Famous Foods with text fields for Guest Name (bound to $/reservation/name), "
            "Guests (bound to $/reservation/guests), Time (bound to $/reservation/time), "
            "and Dietary Notes (bound to $/reservation/notes), pre-filled for Alice, "
            "3 guests, 7:30 PM, and 'No peanuts', plus a primary 'Confirm Booking' button "
            "(firing event 'confirm' with context $/reservation) and a 'Cancel' button (firing event 'cancel')."
        ),
        "express_dsl": """<a2ui>
surface("booking", sendDataModel=true)
$/reservation/name = "Alice"
$/reservation/guests = "3"
$/reservation/time = "7:30 PM"
$/reservation/notes = "No peanuts"
root = Card(main_col)
main_col = Column([title, subtitle, divider, name_field, row_fields, notes_field, actions])
title = Text("Confirm Reservation", "h2")
subtitle = Text("Xi'an Famous Foods • Friday Evening", "caption")
divider = Divider()
name_field = TextField("Guest Name", $/reservation/name, [?required("Guest name is required")])
row_fields = Row([guests_field, time_field])
guests_field = TextField("Party Size", $/reservation/guests)
time_field = TextField("Time", $/reservation/time)
notes_field = TextField("Dietary Notes", $/reservation/notes)
actions = Row([confirm_btn, cancel_btn], "end")
confirm_btn = Button(Text("Confirm Booking"), "primary", Event("confirm", {reservation: $/reservation}))
cancel_btn = Button(Text("Cancel"), _, Event("cancel", {}))
</a2ui>""",
    },
    "login_form": {
        "id": "login_form",
        "title": "Login Form with Validation",
        "description": "Sign-in card from the A2UI Gallery using client-side validation rules (?required, ?email, ?length).",
        "prompt": (
            "Create a login form card on surface 'login_form' with title 'Welcome back' (h2), "
            "subtitle 'Sign in to your account' (caption), an Email TextField bound to $/email "
            "(with required and email validation checks), an obscured Password TextField bound to $/password "
            "(with required and min length 8 checks), a primary 'Sign in' button firing 'login' event "
            "with email context, a Divider, and a bottom row with 'Don't have an account?' and a 'Sign up' button."
        ),
        "express_dsl": """<a2ui>
surface("login_form", sendDataModel=true)
$/email = "alice@example.com"
$/password = ""
root = Card(main_column)
main_column = Column([header, email_field, password_field, login_btn, divider, signup_row])
header = Column([title, subtitle], _, "center")
title = Text("Welcome back", "h2")
subtitle = Text("Sign in to your account", "caption")
email_field = TextField("Email", $/email, [?required("Email is required"), ?email("Please enter a valid email address")])
password_field = TextField("Password", $/password, "obscured", [?required("Password is required"), ?length(8, _, "Password must be at least 8 characters long")])
login_btn = Button(Text("Sign in"), "primary", Event("login", {email: $/email}), ?and([email($/email), length($/password, 8)], "Enter a valid email and 8+ character password"))
divider = Divider()
signup_row = Row([Text("Don't have an account?", "caption"), Button(Text("Sign up"), _, Event("signup", {}))], "center", "center")
</a2ui>""",
    },
    "notification_card": {
        "id": "notification_card",
        "title": "Notification Permission Card (Blog Example)",
        "description": "The exact Notification Permission card featured in the Google Developers A2UI Express blog post.",
        "prompt": (
            "Create a notification permission card on surface 'gallery_notification_permission' "
            "with a centered column containing a 'check' Icon (bound to $/icon), an h3 Text title "
            "(bound to $/title = 'Enable notification'), a body Text description "
            "(bound to $/description = 'Get alerts for order status changes'), and a centered Row "
            "of two buttons: 'Yes' (firing 'accept' event) and 'No' (firing 'decline' event)."
        ),
        "express_dsl": """<a2ui>
surface("gallery_notification_permission", sendDataModel=true)
$/description = "Get alerts for order status changes"
$/icon = "check"
$/title = "Enable notification"
root = Card(main_column)
main_column = Column([icon, title, description, actions], _, "center")
icon = Icon($/icon)
title = Text($/title, "h3")
description = Text($/description, "body")
actions = Row([yes_btn, no_btn], "center")
yes_btn_text = Text("Yes")
yes_btn = Button(yes_btn_text, "primary", Event("accept", {}))
no_btn_text = Text("No")
no_btn = Button(no_btn_text, _, Event("decline", {}))
</a2ui>""",
    },
}

CATALOG = BasicCatalog(ProtocolVersion.V0_9)
CAPABILITIES = {"v0.9": {"supportedCatalogIds": [CATALOG.catalog_id]}}

FORMAT_SPECS = {
    "direct_json": {
        "key": "direct_json",
        "title": "Direct JSON",
        "subtitle": "Standard Wire JSON",
        "badge": "DirectJsonFormatFactory",
        "sentinel_tag": "<a2ui-json>",
        "factory": DirectJsonFormatFactory(),
        "sdk_code": """from a2ui.inference_formats import DirectJsonFormatFactory, to_message_dicts
from a2ui.processor import A2uiGenerator, CatalogConfig

generator = A2uiGenerator(
    [CatalogConfig(BasicCatalog(ProtocolVersion.V0_9))],
    examples=[example_models],
    inference_format_factory=DirectJsonFormatFactory(),  # Legacy Direct JSON
)
processor = generator.create_processor(client_capabilities)

# 1. Inject JSON Schema instructions into LLM system prompt
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=user_prompt,
    config=GenerateContentConfig(system_instruction=processor.prompt_snippet),
)

# 2. Parse & validate <a2ui-json> output into A2UI Wire JSON
parts = processor.parse_response(response.text)
wire_json = [m for p in parts if isinstance(p, A2uiPart) for m in to_message_dicts(p.a2ui)]""",
    },
    "express": {
        "key": "express",
        "title": "A2UI Express (Default)",
        "subtitle": "Python-like Positional DSL",
        "badge": "ExpressFormatFactory",
        "sentinel_tag": "<a2ui>",
        "factory": ExpressFormatFactory(),
        "sdk_code": """from a2ui.inference_formats import ExpressFormatFactory, to_message_dicts
from a2ui.processor import A2uiGenerator, CatalogConfig

generator = A2uiGenerator(
    [CatalogConfig(BasicCatalog(ProtocolVersion.V0_9))],
    examples=[example_models],  # JSON examples auto-decompiled to <a2ui> DSL!
    inference_format_factory=ExpressFormatFactory(),  # Now the default!
)
processor = generator.create_processor(client_capabilities)

# 1. Inject compact function signatures into LLM system prompt
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=user_prompt,
    config=GenerateContentConfig(system_instruction=processor.prompt_snippet),
)

# 2. Compile <a2ui> Express DSL into standard A2UI Wire JSON
parts = processor.parse_response(response.text)
wire_json = [m for p in parts if isinstance(p, A2uiPart) for m in to_message_dicts(p.a2ui)]""",
    },
    "atom": {
        "key": "atom",
        "title": "Atom (S-Expressions)",
        "subtitle": "Lisp-like S-Expression DSL",
        "badge": "AtomFormatFactory",
        "sentinel_tag": "<a2ui>",
        "factory": AtomFormatFactory(),
        "sdk_code": """from a2ui.inference_formats import to_message_dicts
from a2ui.inference_formats.experimental.atom import AtomFormatFactory
from a2ui.processor import A2uiGenerator, CatalogConfig

generator = A2uiGenerator(
    [CatalogConfig(BasicCatalog(ProtocolVersion.V0_9))],
    examples=[example_models],  # JSON examples auto-decompiled to Lisp S-exprs!
    inference_format_factory=AtomFormatFactory(),  # Swappable Atom format
)
processor = generator.create_processor(client_capabilities)

# 1. Inject Atom S-expression instructions into LLM system prompt
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=user_prompt,
    config=GenerateContentConfig(system_instruction=processor.prompt_snippet),
)

# 2. Compile <a2ui> Atom S-expressions into standard A2UI Wire JSON
parts = processor.parse_response(response.text)
wire_json = [m for p in parts if isinstance(p, A2uiPart) for m in to_message_dicts(p.a2ui)]""",
    },
    "elemental": {
        "key": "elemental",
        "title": "Elemental (HTML Elements)",
        "subtitle": "HTML Custom Elements (<ui-*>)",
        "badge": "ElementalFormatFactory",
        "sentinel_tag": "<a2ui>",
        "factory": ElementalFormatFactory(),
        "sdk_code": """from a2ui.inference_formats import to_message_dicts
from a2ui.inference_formats.experimental.elemental import ElementalFormatFactory
from a2ui.processor import A2uiGenerator, CatalogConfig

generator = A2uiGenerator(
    [CatalogConfig(BasicCatalog(ProtocolVersion.V0_9))],
    examples=[example_models],  # JSON examples auto-decompiled to <ui-*> HTML!
    inference_format_factory=ElementalFormatFactory(),  # Swappable Elemental format
)
processor = generator.create_processor(client_capabilities)

# 1. Inject Elemental HTML tag instructions into LLM system prompt
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=user_prompt,
    config=GenerateContentConfig(system_instruction=processor.prompt_snippet),
)

# 2. Compile <a2ui> Elemental HTML into standard A2UI Wire JSON
parts = processor.parse_response(response.text)
wire_json = [m for p in parts if isinstance(p, A2uiPart) for m in to_message_dicts(p.a2ui)]""",
    },
}

# Bootstrap examples from notification_card + login_form
_bootstrap_express_proc = A2uiGenerator(
    [CatalogConfig(CATALOG)],
    inference_format_factory=ExpressFormatFactory(),
).create_processor(CAPABILITIES)

_example_models_list = []
for _ex_id in ("notification_card", "login_form"):
    _parts = _bootstrap_express_proc.parse_response(PRESETS[_ex_id]["express_dsl"])
    _models = []
    for _p in _parts:
        if isinstance(_p, A2uiPart):
            _models.extend(_p.a2ui)
    _example_models_list.append(_models)

PROCESSORS = {}
for _fmt_key, _spec in FORMAT_SPECS.items():
    _gen = A2uiGenerator(
        [CatalogConfig(CATALOG)],
        examples=_example_models_list,
        inference_format_factory=_spec["factory"],
    )
    PROCESSORS[_fmt_key] = _gen.create_processor(CAPABILITIES)

# Populate all 4 format representations for each preset at startup
for _preset in PRESETS.values():
    _parts = PROCESSORS["express"].parse_response(_preset["express_dsl"])
    _models = []
    _msgs = []
    for _p in _parts:
        if isinstance(_p, A2uiPart):
            _models.extend(_p.a2ui)
            _msgs.extend(to_message_dicts(_p.a2ui))

    _preset["formats"] = {
        "direct_json": "<a2ui-json>\n" + json.dumps(_msgs, indent=2) + "\n</a2ui-json>",
        "express": _preset["express_dsl"],
    }
    for _exp_key in ("atom", "elemental"):
        _fmt = FORMAT_SPECS[_exp_key]["factory"].create_format([CATALOG])
        _decompiled = _fmt.create_parser().decompile(_models)
        _preset["formats"][_exp_key] = f"<a2ui>\n{_decompiled}\n</a2ui>"


def extract_wire_messages(parts: list) -> list[dict]:
    msgs = []
    for part in parts:
        if isinstance(part, A2uiPart):
            msgs.extend(to_message_dicts(part.a2ui))
    return msgs


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~3.6 chars/token for code/JSON) when running offline."""
    return max(1, round(len(text) / 3.6))


DEFAULT_MODEL = "gemini-3.8-flash"
DEFAULT_VERTEX_LOCATION = "global"
_ADC_CACHE: tuple[object | None, str | None] | None = None


def _get_adc_credentials() -> tuple[object | None, str | None]:
    global _ADC_CACHE
    if _ADC_CACHE is None:
        try:
            import google.auth

            creds, default_project = google.auth.default()
            _ADC_CACHE = (creds, default_project)
        except Exception:
            _ADC_CACHE = (None, None)
    return _ADC_CACHE


def resolve_genai_auth(
    auth_mode: str = "auto",
    api_key_override: str | None = None,
    project_override: str | None = None,
    location_override: str | None = None,
) -> dict:
    """Resolves either Gemini API Key or Google Cloud / Vertex AI ADC."""
    creds, adc_project = _get_adc_credentials()
    env_project = os.environ.get("GOOGLE_CLOUD_PROJECT") or adc_project
    env_location = os.environ.get("GOOGLE_CLOUD_LOCATION") or DEFAULT_VERTEX_LOCATION

    # Explicit UI overrides
    mode = (auth_mode or "auto").strip().lower()
    if mode == "api_key":
        key = (api_key_override or "").strip()
        if key:
            return {
                "ready": True,
                "mode": "api_key",
                "api_key": key,
                "label": "✓ Gemini API Key Ready (UI)",
            }
        return {
            "ready": False,
            "mode": "none",
            "label": "Enter a Gemini API Key in Credentials",
        }

    if mode == "vertexai":
        proj = (project_override or "").strip() or env_project
        loc = (location_override or "").strip() or env_location
        if creds and proj:
            return {
                "ready": True,
                "mode": "vertexai",
                "project": proj,
                "location": loc,
                "label": f"✓ Vertex AI Ready ({proj} • {loc})",
            }
        if not creds:
            return {
                "ready": False,
                "mode": "none",
                "label": "ADC not found — run `gcloud auth application-default login`",
            }
        return {
            "ready": False,
            "mode": "none",
            "label": "Enter a Google Cloud Project ID in Credentials",
        }

    # Auto mode: check environment variables, then fall back to ADC
    use_vertex_env = os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "").strip().lower()
    raw_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
    valid_key = (
        raw_key
        if (raw_key and not raw_key.startswith("PASTE_") and not raw_key.startswith("your_"))
        else ""
    )

    if use_vertex_env in ("1", "true", "yes"):
        if creds and env_project:
            return {
                "ready": True,
                "mode": "vertexai",
                "project": env_project,
                "location": env_location,
                "label": f"✓ Vertex AI Ready ({env_project} • {env_location})",
            }
        return {
            "ready": False,
            "mode": "none",
            "label": "Configure Credentials (Vertex AI ADC or Gemini API Key)",
        }

    if valid_key:
        return {
            "ready": True,
            "mode": "api_key",
            "api_key": valid_key,
            "label": "✓ Gemini API Key Ready",
        }

    if use_vertex_env not in ("0", "false", "no") and creds and env_project:
        return {
            "ready": True,
            "mode": "vertexai",
            "project": env_project,
            "location": env_location,
            "label": f"✓ Vertex AI Ready ({env_project} • {env_location})",
        }

    return {
        "ready": False,
        "mode": "none",
        "label": "Configure Credentials (Gemini API Key or Vertex AI)",
    }


app = FastAPI(title="A2UI Swappable Inference Formats Explorer")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class CompareRequest(BaseModel):
    preset_id: str = "reservation_form"


class LiveGenerateRequest(BaseModel):
    prompt: str
    model: str = DEFAULT_MODEL
    formats: list[str] = ["direct_json", "express", "atom", "elemental"]
    auth_mode: str = "auto"
    api_key: str | None = None
    project: str | None = None
    location: str | None = None


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/presets")
def get_presets():
    creds, adc_project = _get_adc_credentials()
    auth = resolve_genai_auth()
    json_prompt_chars = len(PROCESSORS["direct_json"].prompt_snippet)
    express_prompt_chars = len(PROCESSORS["express"].prompt_snippet)
    return {
        "default_model": DEFAULT_MODEL,
        "has_api_key": auth["ready"],
        "auth": {
            "ready": auth["ready"],
            "mode": auth["mode"],
            "label": auth["label"],
            "adc_available": creds is not None,
            "default_project": os.environ.get("GOOGLE_CLOUD_PROJECT") or adc_project or "",
            "default_location": os.environ.get("GOOGLE_CLOUD_LOCATION") or DEFAULT_VERTEX_LOCATION,
        },
        "prompt_stats": {
            "direct_json_chars": json_prompt_chars,
            "express_chars": express_prompt_chars,
            "reduction_pct": round(
                (1 - express_prompt_chars / json_prompt_chars) * 100, 1
            ),
        },
        "formats": [
            {
                "key": k,
                "title": s["title"],
                "subtitle": s["subtitle"],
                "badge": s["badge"],
                "sentinel_tag": s["sentinel_tag"],
                "prompt_chars": len(PROCESSORS[k].prompt_snippet),
                "est_input_tokens": estimate_tokens(PROCESSORS[k].prompt_snippet),
            }
            for k, s in FORMAT_SPECS.items()
        ],
        "presets": [
            {
                "id": p["id"],
                "title": p["title"],
                "description": p["description"],
                "prompt": p["prompt"],
            }
            for p in PRESETS.values()
        ],
    }


@app.post("/api/compare-preset")
def compare_preset(req: CompareRequest):
    preset = PRESETS.get(req.preset_id)
    if not preset:
        raise HTTPException(status_code=404, detail=f"Unknown preset: {req.preset_id}")

    results = {}
    for fmt_key, spec in FORMAT_SPECS.items():
        raw_text = preset["formats"][fmt_key]
        processor = PROCESSORS[fmt_key]
        t0 = time.perf_counter()
        parts = processor.parse_response(raw_text)
        parse_ms = (time.perf_counter() - t0) * 1000
        wire_msgs = extract_wire_messages(parts)
        est_out = estimate_tokens(raw_text)
        est_in = estimate_tokens(processor.prompt_snippet)
        sim_latency_s = round(est_out / 160.0, 2)

        results[fmt_key] = {
            "key": fmt_key,
            "title": spec["title"],
            "subtitle": spec["subtitle"],
            "format_name": f"{spec['title']} ({spec['badge']})",
            "badge": spec["badge"],
            "sentinel_tag": spec["sentinel_tag"],
            "sdk_code": spec["sdk_code"],
            "raw_output": raw_text,
            "wire_messages": wire_msgs,
            "error": None,
            "chars": len(raw_text),
            "lines": len(raw_text.splitlines()),
            "input_tokens": est_in,
            "output_tokens": est_out,
            "latency_s": sim_latency_s,
            "parse_ms": round(parse_ms, 2),
        }

    return {
        "mode": "preset",
        "preset": {
            "id": preset["id"],
            "title": preset["title"],
            "description": preset["description"],
            "prompt": preset["prompt"],
        },
        "formats": results,
        # Backwards-compatible top-level aliases
        "direct_json": results["direct_json"],
        "express": results["express"],
        "atom": results["atom"],
        "elemental": results["elemental"],
    }


@app.post("/api/generate-live")
def generate_live(req: LiveGenerateRequest):
    auth = resolve_genai_auth(
        auth_mode=req.auth_mode,
        api_key_override=req.api_key,
        project_override=req.project,
        location_override=req.location,
    )
    if not auth["ready"]:
        raise HTTPException(
            status_code=400,
            detail=auth["label"],
        )

    from google import genai
    from google.genai import types

    if auth["mode"] == "vertexai":
        client = genai.Client(
            vertexai=True,
            project=auth["project"],
            location=auth["location"],
        )
    else:
        client = genai.Client(api_key=auth["api_key"], vertexai=False)

    role_instruction = (
        "You are an A2UI assistant. Respond ONLY with the requested A2UI UI block "
        "using components from the Basic Catalog. Do not include conversational text outside the tags."
    )

    requested_keys = [k for k in req.formats if k in FORMAT_SPECS] or list(FORMAT_SPECS.keys())

    def _run_one(fmt_key: str) -> tuple[str, dict]:
        spec = FORMAT_SPECS[fmt_key]
        processor = PROCESSORS[fmt_key]
        system_instruction = f"{role_instruction}\n\n{processor.prompt_snippet}"
        t0 = time.perf_counter()
        response = client.models.generate_content(
            model=req.model,
            contents=req.prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        latency_s = time.perf_counter() - t0
        raw_text = (response.text or "").strip()

        t_parse = time.perf_counter()
        try:
            parts = processor.parse_response(raw_text)
            wire_msgs = extract_wire_messages(parts)
            error_msg = None
        except Exception as exc:
            # 1-turn self-correction using the compiler's diagnostic error
            try:
                fix_resp = client.models.generate_content(
                    model=req.model,
                    contents=[
                        types.Content(role="user", parts=[types.Part.from_text(text=req.prompt)]),
                        types.Content(role="model", parts=[types.Part.from_text(text=raw_text)]),
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_text(
                                    text=f"Compiler error: {exc}\nOutput the corrected A2UI block."
                                )
                            ],
                        ),
                    ],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.0,
                        thinking_config=types.ThinkingConfig(thinking_budget=0),
                    ),
                )
                latency_s = time.perf_counter() - t0
                raw_text = (fix_resp.text or "").strip()
                parts = processor.parse_response(raw_text)
                wire_msgs = extract_wire_messages(parts)
                error_msg = None
                response = fix_resp
            except Exception as exc2:
                wire_msgs = []
                error_msg = str(exc2)
        parse_ms = (time.perf_counter() - t_parse) * 1000

        usage = response.usage_metadata
        return fmt_key, {
            "key": fmt_key,
            "title": spec["title"],
            "subtitle": spec["subtitle"],
            "format_name": f"{spec['title']} ({spec['badge']})",
            "badge": spec["badge"],
            "sentinel_tag": spec["sentinel_tag"],
            "sdk_code": spec["sdk_code"],
            "raw_output": raw_text,
            "wire_messages": wire_msgs,
            "error": error_msg,
            "chars": len(raw_text),
            "lines": len(raw_text.splitlines()),
            "input_tokens": usage.prompt_token_count if usage else estimate_tokens(system_instruction),
            "output_tokens": usage.candidates_token_count if usage else estimate_tokens(raw_text),
            "latency_s": round(latency_s, 2),
            "parse_ms": round(parse_ms, 2),
        }

    out = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for k, res in pool.map(_run_one, requested_keys):
            out[k] = res

    return {
        "mode": "live",
        "model": req.model,
        "prompt": req.prompt,
        "formats": out,
        "direct_json": out.get("direct_json"),
        "express": out.get("express"),
        "atom": out.get("atom"),
        "elemental": out.get("elemental"),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Start the A2UI Swappable Inference Formats side-by-side comparison web server."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind (default: 8080)")
    args = parser.parse_args()

    print(f"Starting A2UI Express vs. Direct JSON Explorer at http://{args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
