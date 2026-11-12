"""Sample 2: Multimodal Decisions across Images, Audio, Video, PDFs & Cross-Modal Fusion.

Gemini Decision 1 (`gemini-decision-1`) natively evaluates multimodal inputs in a
single forward pass—with no separate OCR or Speech-to-Text step and 0 output tokens.

Examples included:
  1. `image_decision`      : Public image URI + text note (`noul`, `choice`, `score`).
  2. `image_resolution`    : Compare `resolution="low"` vs `"high"` token cost & confidence.
  3. `audio_decision`      : MP3 clip (`audio/mp3`) evaluated directly without transcription.
  4. `video_decision`      : MP4 video (`video/mp4`) evaluated for safety/scene classification.
  5. `pdf_decision`        : Local PDF invoice (`application/pdf`) evaluated without OCR.
  6. `cross_modal_claim`   : Combine PDF invoice + damage photo + claim text in one pass.

Usage:
    python 02_multimodal.py                    # Run all 6 multimodal examples
    python 02_multimodal.py image_decision
    python 02_multimodal.py image_resolution
    python 02_multimodal.py audio_decision
    python 02_multimodal.py video_decision
    python 02_multimodal.py pdf_decision
    python 02_multimodal.py cross_modal_claim
"""

import base64
import os
from pathlib import Path
import sys
import time
import warnings

warnings.filterwarnings("ignore", category=SyntaxWarning, module=r"google\.genai.*")

from google import genai

MODEL = "gemini-decision-1"
ASSETS_DIR = Path(__file__).parent / "assets"

SPILL_IMAGE_URL = "https://storage.googleapis.com/generativeai-downloads/images/spill.jpg"
APOLLO_AUDIO_URL = "https://storage.googleapis.com/generativeai-downloads/data/Apollo-11_Day-01-Highlights-10s.mp3"
BLAZES_VIDEO_URL = "https://storage.googleapis.com/generativeai-downloads/videos/ForBiggerBlazes.mp4"


def get_client() -> genai.Client:
    """Create a Gemini client targeting v1beta (required for the Decisions API)."""
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        sys.exit(
            "Error: Set GEMINI_API_KEY (or GOOGLE_API_KEY) before running.\n"
            "  export GEMINI_API_KEY='your-api-key'"
        )
    return genai.Client(http_options={"api_version": "v1beta"})


def print_usage(result, elapsed_ms: float) -> None:
    """Print latency and per-modality input token breakdown."""
    usage = result.usage
    modalities = ", ".join(
        f"{m.modality}={m.tokens}" for m in (usage.input_tokens_by_modality or [])
    )
    print(
        f"  [Telemetry] latency={elapsed_ms:.0f}ms | "
        f"input_tokens={usage.total_input_tokens} ({modalities}) | "
        f"output_tokens={usage.total_output_tokens}"
    )


def image_decision() -> None:
    """1. Image URI + text note evaluated across `noul`, `choice`, and `score`."""
    print("\n=== 1. Image + Text (`image` URI) ===")
    client = get_client()

    note = "Breakroom counter check 10 minutes before the 9 AM client meeting."
    print(f"  Image: {SPILL_IMAGE_URL}")
    print(f"  Note:  {note!r}")

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=[
            {
                "type": "image",
                "uri": SPILL_IMAGE_URL,
                "mime_type": "image/jpeg",
                "resolution": "low",
            },
            {"type": "text", "text": note},
        ],
        questions={
            "has_spill": {
                "type": "noul",
                "instructions": "Is there an uncleaned liquid spill on the counter?",
            },
            "next_action": {
                "type": "choice",
                "instructions": "Which cleanup action fits the scene?",
                "criteria": {
                    "wipe_with_cloth": "Small counter spill with a cloth or towel nearby.",
                    "dispatch_janitorial": "Large floor hazard, broken glass, or active leak.",
                    "ready_for_meeting": "Counter is clean and ready for guests.",
                },
            },
            "mess_severity": {
                "type": "score",
                "instructions": "Rate the severity of the counter mess.",
                "criteria": [
                    "Clean and guest-ready.",
                    "Minor localized counter spill.",
                    "Major spill or safety hazard.",
                ],
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    a = result.answers
    print(f"  has_spill     -> P(yes)={a['has_spill'].noul:.2f} (conf={a['has_spill'].confidence:.2f})")
    print(f"  next_action   -> {a['next_action'].choice!r} (conf={a['next_action'].confidence:.2f})")
    print(f"  mess_severity -> score={a['mess_severity'].score:.2f}/2 (conf={a['mess_severity'].confidence:.2f})")
    print_usage(result, elapsed_ms)


def image_resolution() -> None:
    """2. Compare `resolution='low'` vs `'high'` on a local product photo."""
    print("\n=== 2. Image Media Resolution (`low` vs `high` token cost) ===")
    client = get_client()

    image_path = ASSETS_DIR / "cracked_monitor.jpg"
    image_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    print(f"  Local image: {image_path.name} ({image_path.stat().st_size // 1024} KB)")

    # Supported image resolutions: "low", "medium", "high", "ultra_high"
    for resolution in ("low", "high"):
        t0 = time.perf_counter()
        result = client.decisions.create(
            model=MODEL,
            input=[
                {
                    "type": "image",
                    "data": image_b64,
                    "mime_type": "image/jpeg",
                    "resolution": resolution,
                },
            ],
            questions={
                "screen_cracked": {
                    "type": "noul",
                    "instructions": "Does the monitor screen show spiderweb cracks or shattered glass?",
                },
                "usb_cable_visible": {
                    "type": "noul",
                    "instructions": "Is a detached USB-C cable visible on the desk next to the box?",
                },
            },
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        a = result.answers
        print(
            f"  resolution={resolution:<6} -> "
            f"P(cracked)={a['screen_cracked'].noul:.2f}, "
            f"P(cable_visible)={a['usb_cable_visible'].noul:.2f}"
        )
        print_usage(result, elapsed_ms)


def audio_decision() -> None:
    """3. Direct audio classification (`audio/mp3`) with no Speech-to-Text step."""
    print("\n=== 3. Audio Clip (`audio/mp3` — Zero Separate Transcription Cost) ===")
    client = get_client()
    print(f"  Audio: {APOLLO_AUDIO_URL}")

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=[
            {
                "type": "audio",
                "uri": APOLLO_AUDIO_URL,
                "mime_type": "audio/mp3",
            },
        ],
        questions={
            "mentions_spaceflight": {
                "type": "noul",
                "instructions": "Is the speaker talking about spaceflight or a rocket launch?",
            },
            "broadcast_domain": {
                "type": "choice",
                "instructions": "Which topic category best matches this audio clip?",
                "criteria": {
                    "aerospace_mission": "Rocket launch, mission control, or spaceflight telemetry.",
                    "financial_earnings": "Quarterly earnings call or stock market commentary.",
                    "sports_commentary": "Live play-by-play of a sporting event.",
                    "other": "Any other audio topic.",
                },
            },
            "audio_intelligibility": {
                "type": "score",
                "instructions": "Rate how intelligible the spoken words are in this recording.",
                "criteria": [
                    "Unintelligible noise or static.",
                    "Radio/archival bandwidth with understandable speech.",
                    "Studio-grade crystal-clear modern voice recording.",
                ],
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    a = result.answers
    print(
        f"  mentions_spaceflight  -> P(yes)={a['mentions_spaceflight'].noul:.2f} "
        f"(conf={a['mentions_spaceflight'].confidence:.2f})"
    )
    print(
        f"  broadcast_domain      -> {a['broadcast_domain'].choice!r} "
        f"(conf={a['broadcast_domain'].confidence:.2f})"
    )
    print(
        f"  audio_intelligibility -> score={a['audio_intelligibility'].score:.2f}/2 "
        f"(conf={a['audio_intelligibility'].confidence:.2f})"
    )
    print_usage(result, elapsed_ms)


def video_decision() -> None:
    """4. Direct video evaluation (`video/mp4`, `resolution='low'`)."""
    print("\n=== 4. Video Clip (`video/mp4` at `resolution='low'`) ===")
    client = get_client()
    print(f"  Video: {BLAZES_VIDEO_URL}")

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=[
            {
                "type": "video",
                "uri": BLAZES_VIDEO_URL,
                "mime_type": "video/mp4",
                "resolution": "low",  # Supported for video: "low", "medium", "high"
            },
        ],
        questions={
            "shows_fire": {
                "type": "noul",
                "instructions": "Does the video show fire or open flames?",
            },
            "ad_placement_suitability": {
                "type": "choice",
                "instructions": "Which brand-safety tier fits this video clip?",
                "criteria": {
                    "family_friendly_promo": "Commercial or entertainment promo with no graphic violence.",
                    "sensitive_hazard_news": "Real-world disaster, emergency, or graphic incident.",
                    "instructional_tutorial": "Step-by-step software or DIY screencast.",
                    "other": "Anything outside these categories.",
                },
            },
            "visual_pacing": {
                "type": "score",
                "instructions": "Rate the visual pacing and motion intensity of the video.",
                "criteria": [
                    "Static slide or talking head with minimal motion.",
                    "Moderate camera movement and scene cuts.",
                    "Fast-paced dramatic cuts and high visual intensity.",
                ],
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    a = result.answers
    print(f"  shows_fire               -> P(yes)={a['shows_fire'].noul:.2f} (conf={a['shows_fire'].confidence:.2f})")
    print(
        f"  ad_placement_suitability -> {a['ad_placement_suitability'].choice!r} "
        f"(conf={a['ad_placement_suitability'].confidence:.2f})"
    )
    print(
        f"  visual_pacing            -> score={a['visual_pacing'].score:.2f}/2 "
        f"(conf={a['visual_pacing'].confidence:.2f})"
    )
    print_usage(result, elapsed_ms)


def pdf_decision() -> None:
    """5. Direct PDF document evaluation (`application/pdf`) without separate OCR."""
    print("\n=== 5. PDF Document (`document` / `application/pdf`) ===")
    client = get_client()

    pdf_path = ASSETS_DIR / "warranty_invoice.pdf"
    pdf_b64 = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")
    print(f"  Local PDF: {pdf_path.name} ({pdf_path.stat().st_size} bytes)")

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=[
            {
                "type": "document",
                "data": pdf_b64,
                "mime_type": "application/pdf",
            },
        ],
        questions={
            "is_paid_in_full": {
                "type": "noul",
                "instructions": "Does the invoice state that payment has been paid in full?",
            },
            "includes_damage_protection": {
                "type": "noul",
                "instructions": "Does the invoice include transit or accidental screen damage protection?",
            },
            "expense_category": {
                "type": "choice",
                "instructions": "Which corporate expense category fits this receipt?",
                "criteria": {
                    "computer_hardware": "Monitors, laptops, docks, and peripherals.",
                    "travel_lodging": "Flights, hotels, trains, and meals.",
                    "software_saas": "Cloud subscriptions and software licenses.",
                    "other": "Other business expenses.",
                },
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    a = result.answers
    print(
        f"  is_paid_in_full            -> P(yes)={a['is_paid_in_full'].noul:.2f} "
        f"(conf={a['is_paid_in_full'].confidence:.2f})"
    )
    print(
        f"  includes_damage_protection -> P(yes)={a['includes_damage_protection'].noul:.2f} "
        f"(conf={a['includes_damage_protection'].confidence:.2f})"
    )
    print(
        f"  expense_category           -> {a['expense_category'].choice!r} "
        f"(conf={a['expense_category'].confidence:.2f})"
    )
    # Note: PDF page images are counted under the `image` modality in usage telemetry.
    print_usage(result, elapsed_ms)


def cross_modal_claim() -> None:
    """6. Cross-modal fusion: combine a PDF invoice + damage photo + claim text in 1 pass."""
    print("\n=== 6. Cross-Modal Fusion (`PDF` + `Image` + `Text` in One Pass) ===")
    client = get_client()

    pdf_path = ASSETS_DIR / "warranty_invoice.pdf"
    photo_path = ASSETS_DIR / "cracked_monitor.jpg"
    claim_note = (
        "Warranty claim for Order ORD-8821: My 15-inch USB-C portable monitor arrived "
        "with a shattered left screen. Attaching my paid invoice PDF and a photo of the screen."
    )

    print(f"  Inputs: {pdf_path.name} + {photo_path.name} + claim text")

    t0 = time.perf_counter()
    result = client.decisions.create(
        model=MODEL,
        input=[
            {
                "type": "document",
                "data": base64.b64encode(pdf_path.read_bytes()).decode("utf-8"),
                "mime_type": "application/pdf",
            },
            {
                "type": "image",
                "data": base64.b64encode(photo_path.read_bytes()).decode("utf-8"),
                "mime_type": "image/jpeg",
                "resolution": "low",
            },
            {
                "type": "text",
                "text": claim_note,
            },
        ],
        questions={
            "order_id_matches_pdf": {
                "type": "noul",
                "instructions": "Does the order ID mentioned in the claim text match the Order ID on the PDF invoice?",
            },
            "photo_matches_invoiced_product": {
                "type": "noul",
                "instructions": "Does the product shown in the photo match the portable monitor listed on the PDF invoice?",
            },
            "photo_verifies_screen_damage": {
                "type": "noul",
                "instructions": "Does the photo confirm visible cracks/shattering on the monitor screen?",
            },
            "claim_decision": {
                "type": "choice",
                "instructions": "Based on the PDF policy, invoice status, and photo evidence, what is the right claim outcome?",
                "criteria": {
                    "approve_instant_replacement": "Paid invoice covers screen damage, item matches, and photo confirms damage.",
                    "reject_unverified_damage": "Photo shows an undamaged screen or wrong product.",
                    "manual_adjuster_review": "Documents conflict or policy coverage is unclear.",
                },
            },
        },
    )
    elapsed_ms = (time.perf_counter() - t0) * 1000

    a = result.answers
    print(
        f"  order_id_matches_pdf           -> P(yes)={a['order_id_matches_pdf'].noul:.2f} "
        f"(conf={a['order_id_matches_pdf'].confidence:.2f})"
    )
    print(
        f"  photo_matches_invoiced_product -> P(yes)={a['photo_matches_invoiced_product'].noul:.2f} "
        f"(conf={a['photo_matches_invoiced_product'].confidence:.2f})"
    )
    print(
        f"  photo_verifies_screen_damage   -> P(yes)={a['photo_verifies_screen_damage'].noul:.2f} "
        f"(conf={a['photo_verifies_screen_damage'].confidence:.2f})"
    )
    print(
        f"  claim_decision                 -> {a['claim_decision'].choice!r} "
        f"(conf={a['claim_decision'].confidence:.2f})"
    )
    print_usage(result, elapsed_ms)


SAMPLES = {
    "image_decision": image_decision,
    "image_resolution": image_resolution,
    "audio_decision": audio_decision,
    "video_decision": video_decision,
    "pdf_decision": pdf_decision,
    "cross_modal_claim": cross_modal_claim,
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
