"""ADK Shopping Agent that interacts with a UCP Merchant Server."""

import os
from typing import Any

import httpx
from google.adk.agents import Agent
from ucp_sdk.models.schemas.profile import BusinessSchema as BusinessProfile
from ucp_sdk.models.schemas.shopping.checkout import Checkout

UCP_SERVER_URL = os.environ.get("UCP_SERVER_URL", "http://127.0.0.1:8182")
UCP_HEADERS = {
    "UCP-Agent": 'profile="https://agent.example.com/.well-known/ucp-agent.json"',
}


def discover_merchant() -> dict[str, Any]:
    """Discover the merchant's UCP capabilities, services, and payment handlers via /.well-known/ucp."""
    with httpx.Client(base_url=UCP_SERVER_URL, headers=UCP_HEADERS, timeout=10.0) as client:
        resp = client.get("/.well-known/ucp")
        resp.raise_for_status()
        profile = BusinessProfile.model_validate(resp.json())
        return {
            "version": profile.ucp.version,
            "services": list(profile.ucp.services.keys()),
            "capabilities": list((profile.ucp.capabilities or {}).keys()),
            "payment_handlers": list(profile.ucp.payment_handlers.keys()),
            "available_skus": [
                {"sku": "sku_roses", "title": "Red Roses Bouquet", "price": "$25.00"},
                {"sku": "sku_vase", "title": "Ceramic Vase", "price": "$15.00"},
            ],
        }


def create_checkout_session(sku: str, quantity: int = 1) -> dict[str, Any]:
    """Create a new UCP checkout session for the given product SKU and quantity.

    Args:
        sku: The product SKU (e.g. 'sku_roses' or 'sku_vase').
        quantity: Number of items to purchase.
    """
    with httpx.Client(base_url=UCP_SERVER_URL, headers=UCP_HEADERS, timeout=10.0) as client:
        resp = client.post(
            "/checkout-sessions",
            json={
                "items": [{"sku": sku, "quantity": quantity}],
                "platform_capabilities": [
                    "dev.ucp.shopping.checkout",
                    "dev.ucp.shopping.fulfillment",
                    "dev.ucp.shopping.discount",
                ],
            },
        )
        resp.raise_for_status()
        checkout = Checkout.model_validate(resp.json())
        return checkout.model_dump(by_alias=True, exclude_none=True, mode="json")


def update_checkout_session(
    checkout_id: str,
    buyer_email: str,
    shipping_method: str = "Express Delivery",
    discount_code: str | None = None,
) -> dict[str, Any]:
    """Update a UCP checkout session with buyer email, shipping method, and optional discount code.

    Args:
        checkout_id: The UCP checkout session ID (e.g. 'chk_...').
        buyer_email: Buyer's email address.
        shipping_method: Delivery option (e.g. 'Standard Shipping' or 'Express Delivery').
        discount_code: Optional promo code (e.g. 'SAVE10').
    """
    with httpx.Client(base_url=UCP_SERVER_URL, headers=UCP_HEADERS, timeout=10.0) as client:
        resp = client.put(
            f"/checkout-sessions/{checkout_id}",
            json={
                "buyer_email": buyer_email,
                "shipping_method": shipping_method,
                "discount_code": discount_code,
            },
        )
        resp.raise_for_status()
        checkout = Checkout.model_validate(resp.json())
        return checkout.model_dump(by_alias=True, exclude_none=True, mode="json")


def complete_checkout_session(
    checkout_id: str,
    payment_handler: str = "com.google.pay",
    payment_token: str = "tok_gpay_demo_123",
) -> dict[str, Any]:
    """Complete a ready UCP checkout session using a payment handler and tokenized instrument.

    Args:
        checkout_id: The UCP checkout session ID.
        payment_handler: Negotiated payment handler (e.g. 'com.google.pay' or 'dev.shopify.shop_pay').
        payment_token: Tokenized payment credential from the credential provider.
    """
    with httpx.Client(base_url=UCP_SERVER_URL, headers=UCP_HEADERS, timeout=10.0) as client:
        resp = client.post(
            f"/checkout-sessions/{checkout_id}/complete",
            json={
                "payment_handler": payment_handler,
                "payment_token": payment_token,
            },
        )
        resp.raise_for_status()
        checkout = Checkout.model_validate(resp.json())
        return checkout.model_dump(by_alias=True, exclude_none=True, mode="json")


root_agent = Agent(
    name="ucp_shopping_agent",
    model="gemini-2.5-flash",
    description="AI Shopping Agent that discovers merchants and completes purchases using the Universal Commerce Protocol (UCP).",
    instruction="""
You are a helpful AI Shopping Agent that uses the Universal Commerce Protocol (UCP).
1. When a user wants to shop or asks what the store supports, call `discover_merchant` first to inspect `/.well-known/ucp`.
2. To start a purchase, call `create_checkout_session` with the requested SKU and quantity.
3. Before completing checkout, ensure buyer email and shipping method (plus any promo code like `SAVE10`) are set using `update_checkout_session` so the session reaches `ready_for_complete`.
4. Finally, call `complete_checkout_session` and share the order ID and permalink URL with the user.
Always format minor currency units (cents) as dollars (e.g. 2500 -> $25.00).
""",
    tools=[
        discover_merchant,
        create_checkout_session,
        update_checkout_session,
        complete_checkout_session,
    ],
)
