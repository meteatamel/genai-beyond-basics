"""Minimal UCP Merchant Server using FastAPI and the official ucp-sdk.

Exposes:
- GET  /.well-known/ucp                      (Discovery profile & signing keys)
- POST /checkout-sessions                    (Create checkout session + capability negotiation)
- PUT  /checkout-sessions/{checkout_id}      (Update checkout with fulfillment & discount)
- POST /checkout-sessions/{checkout_id}/complete (Complete checkout with payment token)
"""

import uuid
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from ucp_sdk.models.schemas.profile import BusinessSchema as BusinessProfile
from ucp_sdk.models.schemas.shopping.checkout import Checkout

app = FastAPI(title="UCP Hello World Merchant Server")

UCP_VERSION = "2026-08-25"

CATALOG = {
    "sku_roses": {"id": "sku_roses", "title": "Red Roses Bouquet", "price": 2500},
    "sku_vase": {"id": "sku_vase", "title": "Ceramic Vase", "price": 1500},
}

MERCHANT_CAPABILITIES = {
    "dev.ucp.shopping.checkout": [
        {
            "version": UCP_VERSION,
            "spec": f"https://ucp.dev/{UCP_VERSION}/specification/shopping/checkout",
            "schema": f"https://ucp.dev/{UCP_VERSION}/schemas/shopping/checkout.json",
        }
    ],
    "dev.ucp.shopping.fulfillment": [
        {
            "version": UCP_VERSION,
            "spec": f"https://ucp.dev/{UCP_VERSION}/specification/shopping/extensions/fulfillment",
            "schema": f"https://ucp.dev/{UCP_VERSION}/schemas/shopping/fulfillment.json",
            "extends": "dev.ucp.shopping.checkout",
        }
    ],
    "dev.ucp.shopping.discount": [
        {
            "version": UCP_VERSION,
            "spec": f"https://ucp.dev/{UCP_VERSION}/specification/shopping/extensions/discount",
            "schema": f"https://ucp.dev/{UCP_VERSION}/schemas/shopping/discount.json",
            "extends": "dev.ucp.shopping.checkout",
        }
    ],
}

PAYMENT_HANDLERS = {
    "com.google.pay": [
        {
            "id": "gpay",
            "version": UCP_VERSION,
            "spec": "https://payments.google.com/gpay/specification",
            "schema": "https://payments.google.com/gpay/schema.json",
        }
    ],
    "dev.shopify.shop_pay": [
        {
            "id": "shop_pay",
            "version": UCP_VERSION,
            "spec": "https://shopify.dev/ucp/shop-pay",
            "schema": "https://shopify.dev/ucp/shop-pay.json",
        }
    ],
}

CHECKOUT_STORE: dict[str, dict[str, Any]] = {}


class LineItemInput(BaseModel):
    sku: str
    quantity: int = 1


class CreateCheckoutInput(BaseModel):
    items: list[LineItemInput]
    platform_capabilities: list[str] | None = None


class UpdateCheckoutInput(BaseModel):
    buyer_email: str | None = None
    shipping_method: str | None = None
    discount_code: str | None = None


class CompleteCheckoutInput(BaseModel):
    payment_handler: str
    payment_token: str


def negotiate_capabilities(requested: list[str] | None) -> dict[str, Any]:
    """Server-selects capability intersection + orphan extension pruning."""
    if requested is None:
        active_names = set(MERCHANT_CAPABILITIES.keys())
    else:
        active_names = set(MERCHANT_CAPABILITIES.keys()) & set(requested)

    # Prune extensions whose parent capability is not in the intersection
    pruned = True
    while pruned:
        pruned = False
        for name in list(active_names):
            parent = MERCHANT_CAPABILITIES[name][0].get("extends")
            if parent and parent not in active_names:
                active_names.remove(name)
                pruned = True

    return {k: MERCHANT_CAPABILITIES[k] for k in MERCHANT_CAPABILITIES if k in active_names}


@app.get("/.well-known/ucp")
def get_ucp_profile() -> dict[str, Any]:
    """Publish the Business UCP Discovery Profile at /.well-known/ucp."""
    profile_data = {
        "ucp": {
            "version": UCP_VERSION,
            "services": {
                "dev.ucp.shopping": [
                    {
                        "version": UCP_VERSION,
                        "spec": f"https://ucp.dev/{UCP_VERSION}/specification/overview",
                        "transport": "rest",
                        "schema": f"https://ucp.dev/{UCP_VERSION}/services/shopping/rest.openapi.json",
                        "endpoint": "http://127.0.0.1:8182",
                    }
                ]
            },
            "capabilities": MERCHANT_CAPABILITIES,
            "payment_handlers": PAYMENT_HANDLERS,
        },
        "keys": [
            {
                "kid": "merchant_key_2026",
                "kty": "EC",
                "crv": "P-256",
                "x": "WbbXwVYGdJoP4Xm3qCkGvBRcRvKtEfXDbWvPzpPS8LA",
                "y": "sP4jHHxYqC89HBo8TjrtVOAGHfJDflYxw7MFMxuFMPY",
                "use": "sig",
                "alg": "ES256",
            }
        ],
    }
    # Validate against official UCP BusinessProfile Pydantic model
    validated = BusinessProfile.model_validate(profile_data)
    return validated.model_dump(by_alias=True, exclude_none=True)


@app.post("/checkout-sessions")
def create_checkout(
    req: CreateCheckoutInput,
    ucp_agent: str | None = Header(default=None, alias="UCP-Agent"),
) -> dict[str, Any]:
    """Create a new UCP Checkout session (`status = incomplete`)."""
    checkout_id = f"chk_{uuid.uuid4().hex[:8]}"
    line_items = []
    subtotal = 0

    for idx, entry in enumerate(req.items, start=1):
        product = CATALOG.get(entry.sku)
        if not product:
            raise HTTPException(status_code=404, detail=f"Unknown SKU: {entry.sku}")
        line_total = product["price"] * entry.quantity
        subtotal += line_total
        line_items.append(
            {
                "id": f"li_{idx}",
                "item": product,
                "quantity": entry.quantity,
                "totals": [
                    {"type": "subtotal", "amount": line_total},
                    {"type": "total", "amount": line_total},
                ],
            }
        )

    active_caps = negotiate_capabilities(req.platform_capabilities)
    checkout_data = {
        "ucp": {
            "version": UCP_VERSION,
            "status": "success",
            "capabilities": active_caps,
            "payment_handlers": PAYMENT_HANDLERS,
        },
        "id": checkout_id,
        "status": "incomplete",
        "currency": "USD",
        "line_items": line_items,
        "totals": [
            {"type": "subtotal", "amount": subtotal},
            {"type": "total", "amount": subtotal},
        ],
        "links": [
            {"type": "terms_of_service", "url": "https://flowershop.example.com/terms"},
            {"type": "privacy_policy", "url": "https://flowershop.example.com/privacy"},
        ],
    }

    validated = Checkout.model_validate(checkout_data)
    dumped = validated.model_dump(by_alias=True, exclude_none=True, mode="json")
    CHECKOUT_STORE[checkout_id] = dumped
    return dumped


@app.put("/checkout-sessions/{checkout_id}")
def update_checkout(checkout_id: str, req: UpdateCheckoutInput) -> dict[str, Any]:
    """Update checkout with fulfillment & discount (`status -> ready_for_complete`)."""
    session = CHECKOUT_STORE.get(checkout_id)
    if not session:
        raise HTTPException(status_code=404, detail="Checkout session not found")

    subtotal = next(t["amount"] for t in session["totals"] if t["type"] == "subtotal")
    totals = [{"type": "subtotal", "amount": subtotal}]
    running_total = subtotal

    if req.discount_code == "SAVE10":
        discount_amount = -int(subtotal * 0.10)  # Negative minor units per UCP spec
        totals.append(
            {
                "type": "discount",
                "display_text": "10% Promo (SAVE10)",
                "amount": discount_amount,
            }
        )
        running_total += discount_amount

    if req.shipping_method:
        shipping_fee = 500  # $5.00
        totals.append(
            {
                "type": "fulfillment",
                "display_text": f"Shipping ({req.shipping_method})",
                "amount": shipping_fee,
            }
        )
        running_total += shipping_fee

    totals.append({"type": "total", "amount": running_total})
    session["totals"] = totals

    if req.buyer_email:
        session["buyer"] = {"email": req.buyer_email}

    if req.buyer_email and req.shipping_method:
        session["status"] = "ready_for_complete"

    validated = Checkout.model_validate(session)
    dumped = validated.model_dump(by_alias=True, exclude_none=True, mode="json")
    CHECKOUT_STORE[checkout_id] = dumped
    return dumped


@app.post("/checkout-sessions/{checkout_id}/complete")
def complete_checkout(checkout_id: str, req: CompleteCheckoutInput) -> dict[str, Any]:
    """Complete checkout with a tokenized payment instrument (`status -> completed`)."""
    session = CHECKOUT_STORE.get(checkout_id)
    if not session:
        raise HTTPException(status_code=404, detail="Checkout session not found")
    if session["status"] != "ready_for_complete":
        raise HTTPException(
            status_code=400,
            detail=f"Checkout is '{session['status']}', expected 'ready_for_complete'",
        )
    if req.payment_handler not in PAYMENT_HANDLERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported payment handler: {req.payment_handler}",
        )

    order_id = f"ord_{uuid.uuid4().hex[:8]}"
    session["status"] = "completed"
    session["order"] = {
        "id": order_id,
        "label": f"Order #{order_id.upper()}",
        "permalink_url": f"https://flowershop.example.com/orders/{order_id}",
    }

    validated = Checkout.model_validate(session)
    dumped = validated.model_dump(by_alias=True, exclude_none=True, mode="json")
    CHECKOUT_STORE[checkout_id] = dumped
    return dumped


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8182)
