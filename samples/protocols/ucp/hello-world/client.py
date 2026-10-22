"""Hello World UCP Client (Platform / Shopping Agent).

Demonstrates the 4-step Universal Commerce Protocol (UCP) journey:
1. Discovery (`GET /.well-known/ucp`)
2. Create Checkout Session & Capability Negotiation (`POST /checkout-sessions`)
3. Update Checkout with Fulfillment & Discount (`PUT /checkout-sessions/{id}`)
4. Complete Checkout with Tokenized Payment (`POST /checkout-sessions/{id}/complete`)

By default, runs in-process against `server.app` so no separate server terminal is required.
Pass `--server_url http://127.0.0.1:8182` to run against an external server process.
"""

import argparse
import asyncio

import httpx
from server import app
from ucp_sdk.models.schemas.profile import BusinessSchema as BusinessProfile
from ucp_sdk.models.schemas.shopping.checkout import Checkout


def format_cents(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    return f"{sign}${abs(cents) / 100:.2f}"


async def run_ucp_flow(server_url: str | None) -> None:
    if server_url:
        transport = None
        base_url = server_url
    else:
        transport = httpx.ASGITransport(app=app)
        base_url = "http://127.0.0.1:8182"

    headers = {
        "UCP-Agent": 'profile="https://agent.example.com/.well-known/ucp-agent.json"',
    }

    async with httpx.AsyncClient(transport=transport, base_url=base_url, headers=headers) as client:
        print("=== 1. UCP Discovery (GET /.well-known/ucp) ===")
        resp = await client.get("/.well-known/ucp")
        resp.raise_for_status()
        profile = BusinessProfile.model_validate(resp.json())
        print(f"Protocol Version:  {profile.ucp.version}")
        print(f"Services:          {list(profile.ucp.services.keys())}")
        print(f"Capabilities:      {list((profile.ucp.capabilities or {}).keys())}")
        print(f"Payment Handlers:  {list(profile.ucp.payment_handlers.keys())}")
        print(f"Signing Key (kid): {profile.keys[0].kid if profile.keys else 'none'}")

        print("\n=== 2. Create Checkout Session (POST /checkout-sessions) ===")
        create_resp = await client.post(
            "/checkout-sessions",
            json={
                "items": [
                    {"sku": "sku_roses", "quantity": 1},  # $25.00
                    {"sku": "sku_vase", "quantity": 1},   # $15.00
                ],
                "platform_capabilities": [
                    "dev.ucp.shopping.checkout",
                    "dev.ucp.shopping.fulfillment",
                    "dev.ucp.shopping.discount",
                ],
            },
        )
        create_resp.raise_for_status()
        checkout = Checkout.model_validate(create_resp.json())
        print(f"Checkout ID:       {checkout.id}")
        print(f"Checkout Status:   {checkout.status}")
        print(f"Negotiated Caps:   {list((checkout.ucp.capabilities or {}).keys())}")
        for li in checkout.line_items:
            print(f"  - {li.quantity}x {li.item.title} ({li.item.id}): {format_cents(li.item.price)}")

        print(f"\n=== 3. Update Checkout: Fulfillment & Discount (PUT /checkout-sessions/{checkout.id}) ===")
        update_resp = await client.put(
            f"/checkout-sessions/{checkout.id}",
            json={
                "buyer_email": "alice@example.com",
                "shipping_method": "Express Delivery",
                "discount_code": "SAVE10",
            },
        )
        update_resp.raise_for_status()
        checkout = Checkout.model_validate(update_resp.json())
        print(f"Checkout Status:   {checkout.status}")
        print("Totals Breakdown:")
        for t in checkout.totals:
            label = t.display_text or t.type.capitalize()
            print(f"  - {label:24s}: {format_cents(t.amount)}")

        print(f"\n=== 4. Complete Checkout (POST /checkout-sessions/{checkout.id}/complete) ===")
        complete_resp = await client.post(
            f"/checkout-sessions/{checkout.id}/complete",
            json={
                "payment_handler": "com.google.pay",
                "payment_token": "tok_gpay_demo_987654",
            },
        )
        complete_resp.raise_for_status()
        checkout = Checkout.model_validate(complete_resp.json())
        print(f"Checkout Status:   {checkout.status}")
        if checkout.order:
            print(f"Order Created:     {checkout.order.label} (id={checkout.order.id})")
            print(f"Order Permalink:   {checkout.order.permalink_url}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run UCP Hello World Client")
    parser.add_argument(
        "--server_url",
        default=None,
        help="Optional URL of a running UCP server (defaults to in-process ASGI server)",
    )
    args = parser.parse_args()
    asyncio.run(run_ucp_flow(args.server_url))


if __name__ == "__main__":
    main()
