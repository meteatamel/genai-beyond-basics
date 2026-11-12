"""Sample 1: Gemini Decisions API fundamentals (text primitives).

Demonstrates the three core question types (`noul`, `choice`, `score`),
disambiguating criteria, and evaluating multiple mixed questions in a single
forward pass using `gemini-decision-1` with zero output tokens.

Usage:
    python 01_basics.py                        # Run all 5 examples
    python 01_basics.py yes_no_basic           # Run a single example
    python 01_basics.py yes_no_criteria
    python 01_basics.py multiple_choice
    python 01_basics.py rubric_score
    python 01_basics.py multi_question_pass
"""

import json
import os
import sys
import time
import warnings

# Suppress upstream invalid escape sequence warning in google-genai 3.2.0 types docstring
warnings.filterwarnings("ignore", category=SyntaxWarning, module=r"google\.genai.*")

from google import genai

MODEL = "gemini-decision-1"


def get_client() -> genai.Client:
    """Create a Gemini client targeting v1beta (required for the Decisions API)."""
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        sys.exit(
            "Error: Set GEMINI_API_KEY (or GOOGLE_API_KEY) before running.\n"
            "  export GEMINI_API_KEY='your-api-key'"
        )
    return genai.Client(http_options={"api_version": "v1beta"})


def print_usage(result, elapsed_ms: float) -> None:
    """Print latency and token usage (highlighting 0 output tokens)."""
    usage = result.usage
    modalities = ", ".join(
        f"{m.modality}={m.tokens}" for m in (usage.input_tokens_by_modality or [])
    )
    print(
        f"  [Telemetry] latency={elapsed_ms:.0f}ms | "
        f"input_tokens={usage.total_input_tokens} ({modalities}) | "
        f"output_tokens={usage.total_output_tokens}"
    )


def yes_no_basic() -> None:
    """1. Basic yes/no (`noul`) question with calibrated probability & confidence."""
    print("\n=== 1. Yes/No (`noul`) — Basic ===")
    client = get_client()

    text = "The blue mug I ordered on Monday arrived cracked on Wednesday."
    print(f"  Input: {text!r}")

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=text,
        questions={
            "is_damaged": {
                "type": "noul",
                "instructions": "Did the item arrive damaged?",
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    ans = result.answers["is_damaged"]
    # Note: noul probabilities always fall in [0.01, 0.99]
    print(
        f"  Answer: P(yes)={ans.noul:.2f} | P(no)={1 - ans.noul:.2f} | "
        f"confidence={ans.confidence:.2f}"
    )
    print_usage(result, elapsed_ms)


def yes_no_criteria() -> None:
    """2. Yes/no (`noul`) with explicit true/false criteria to resolve ambiguity."""
    print("\n=== 2. Yes/No (`noul`) — Disambiguating Criteria ===")
    client = get_client()

    messages = [
        "Customer returned the sweater because they preferred green over blue.",
        "The zipper snapped off the first time I tried the sweater on.",
    ]

    for msg in messages:
        t0 = time.perf_counter()
        result = client.decisions.create(
            model=MODEL,
            input=msg,
            questions={
                "is_defect": {
                    "type": "noul",
                    "instructions": "Is the customer reporting a product defect?",
                    "criteria": {
                        "true_description": "The product itself is broken, torn, or faulty.",
                        "false_description": "Color/style preference, sizing, shipping, or pricing complaint.",
                    },
                },
            },
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        ans = result.answers["is_defect"]
        verdict = "DEFECT" if ans.noul >= 0.70 else "NOT_DEFECT"
        print(f"  Input:   {msg!r}")
        print(
            f"  Verdict: {verdict} (P(yes)={ans.noul:.2f}, confidence={ans.confidence:.2f})"
        )
        print_usage(result, elapsed_ms)


def multiple_choice() -> None:
    """3. Multiple choice (`choice`) across fixed options with probability distribution."""
    print("\n=== 3. Multiple Choice (`choice`) — Ticket Routing ===")
    client = get_client()

    text = "I was charged twice on my Visa card for order #4410."
    print(f"  Input: {text!r}")

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=text,
        questions={
            "department": {
                "type": "choice",
                "instructions": "Which department should handle this request?",
                "criteria": {
                    "billing": "Payments, duplicate charges, invoices, and refunds.",
                    "technical": "Bugs, crashes, or problems using the product.",
                    "shipping": "Delivery delays, lost packages, and tracking.",
                    # Use a non-positional key like 'other' (not 'none_of_the_above')
                    # since option keys are sorted alphabetically before evaluation.
                    "other": "Anything outside billing, technical, or shipping.",
                },
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    ans = result.answers["department"]
    print(f"  Winner: {ans.choice!r} (confidence={ans.confidence:.2f})")
    print("  Probabilities:")
    for option, prob in sorted(ans.probabilities.items(), key=lambda kv: -kv[1]):
        bar = "#" * int(round(prob * 25))
        print(f"    - {option:<10} {prob:6.3f}  {bar}")
    print_usage(result, elapsed_ms)


def rubric_score() -> None:
    """4. Ordered rubric (`score`) returning both continuous score and discrete level."""
    print("\n=== 4. Rubric Rating (`score`) — Issue Severity ===")
    client = get_client()

    text = "CSV export fails in Safari with a blank tab, though downloading in Chrome works."
    print(f"  Input: {text!r}")

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=text,
        questions={
            "severity": {
                "type": "score",
                "instructions": "How severe is this issue for the user?",
                "criteria": [
                    "Cosmetic: visual polish only, no lost functionality.",
                    "Workaround available: a task fails, but an alternative path works.",
                    "Fully blocked: a core task fails with no workaround.",
                ],
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    ans = result.answers["severity"]
    max_index = len(ans.legend) - 1
    normalized = ans.score / max_index
    top_level = max(ans.probabilities, key=ans.probabilities.get)

    print(
        f"  Expected score: {ans.score:.2f} / {max_index} "
        f"(normalized={normalized:.2f}, confidence={ans.confidence:.2f})"
    )
    print(f"  Modal level:    [{top_level}] {ans.legend[top_level]}")
    print("  Level breakdown:")
    for idx, desc in sorted(ans.legend.items(), key=lambda kv: int(kv[0])):
        prob = ans.probabilities.get(idx, 0.0)
        print(f"    - Level {idx}: P={prob:.2f}  ({desc})")
    print_usage(result, elapsed_ms)


def multi_question_pass() -> None:
    """5. Ask mixed `noul`, `choice`, and `score` questions over shared input in 1 pass."""
    print("\n=== 5. Multiple Questions in One Pass (`noul` + `choice` + `score`) ===")
    client = get_client()

    order = {"order": {"id": "8821", "item": "headphones", "price_usd": 240}, "tier": "Gold"}
    message = {"message": "Audio cuts out on the left earcup. Fix it today or I cancel my membership."}

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=[
            {"type": "text", "text": json.dumps(order) + "\n"},
            {"type": "text", "text": json.dumps(message)},
        ],
        questions={
            "is_defect": {
                "type": "noul",
                "instructions": "Does `message` describe a hardware defect?",
            },
            "next_action": {
                "type": "choice",
                "instructions": "What is the right resolution given `tier` and `order`?",
                "criteria": {
                    "instant_refund": "Refund without return. Low value or clear fault.",
                    "replacement_shipment": "Ship a replacement. Customer returns the original.",
                    "troubleshooting_flow": "The issue may be fixable by the customer.",
                    "human_escalation": "High-value dispute or VIP cancellation threat.",
                },
            },
            "churn_risk": {
                "type": "score",
                "instructions": "How likely is the customer to churn if not resolved now?",
                "criteria": [
                    "No churn signal.",
                    "Mild frustration.",
                    "Mentions alternatives.",
                    "Threatens to cancel.",
                ],
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    a = result.answers
    print(f"  is_defect   -> P(yes)={a['is_defect'].noul:.2f} (conf={a['is_defect'].confidence:.2f})")
    print(f"  next_action -> {a['next_action'].choice!r} (conf={a['next_action'].confidence:.2f})")
    print(f"  churn_risk  -> score={a['churn_risk'].score:.2f}/3 (conf={a['churn_risk'].confidence:.2f})")
    print_usage(result, elapsed_ms)


SAMPLES = {
    "yes_no_basic": yes_no_basic,
    "yes_no_criteria": yes_no_criteria,
    "multiple_choice": multiple_choice,
    "rubric_score": rubric_score,
    "multi_question_pass": multi_question_pass,
}


def main() -> None:
    if len(sys.argv) == 1:
        for fn in SAMPLES.values():
            fn()
        return

    arg = sys.argv[1]
    if arg in ("-h", "--help") or arg not in SAMPLES:
        available = ", ".join(SAMPLES.keys())
        print(f"Usage: python {sys.argv[0]} [<sample_name>]")
        print(f"Available samples: {available}")
        sys.exit(0 if arg in ("-h", "--help") else 1)

    SAMPLES[arg]()


if __name__ == "__main__":
    main()
