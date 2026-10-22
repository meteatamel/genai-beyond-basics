# UCP Hello World (Python SDK & FastAPI)

A minimal, self-contained "Hello World" sample using the official [UCP Python SDK](https://github.com/Universal-Commerce-Protocol/python-sdk) (`ucp-sdk`) and FastAPI.

This sample demonstrates the 4-step **Universal Commerce Protocol (UCP)** lifecycle between a **Business (Merchant Server)** and a **Platform (Shopping Agent Client)**:

1. **Discovery (`GET /.well-known/ucp`)**: The client fetches the merchant's UCP profile (`BusinessSchema`), discovering protocol version `2026-08-25`, services (`dev.ucp.shopping`), capabilities (`dev.ucp.shopping.checkout`, `dev.ucp.shopping.fulfillment`, `dev.ucp.shopping.discount`), payment handlers (`com.google.pay`, `dev.shopify.shop_pay`), and ES256 JWK signing keys.
2. **Create Checkout & Capability Negotiation (`POST /checkout-sessions`)**: The client sends line items and its supported capabilities. Using UCP's **server-selects** architecture, the merchant computes the capability intersection, prunes any orphaned extensions, validates the payload against `ucp_sdk.models.schemas.shopping.checkout.Checkout`, and returns a session with `status = "incomplete"`.
3. **Update Checkout (`PUT /checkout-sessions/{id}`)**: The client provides buyer details, selects shipping (`Express Delivery` for `$5.00`), and applies promo code `SAVE10` (`-$4.00` in minor units), transitioning the session to `status = "ready_for_complete"`.
4. **Complete Checkout (`POST /checkout-sessions/{id}/complete`)**: The client submits a tokenized payment instrument for a negotiated payment handler (`com.google.pay`), transitioning the session to `status = "completed"` and returning an `OrderConfirmation` with a permalink URL.

## Run the sample

### Option 1: Single-command run (in-process ASGI server)

By default, [client.py](./client.py) mounts [server.py](./server.py) in-process via `httpx.ASGITransport`, so you can run the entire flow in a single terminal:

```shell
uv run --with ucp-sdk --with fastapi --with httpx python client.py
```

Or with `venv` and `pip`:

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python client.py
```

### Option 2: Separate Server & Client terminals

Start the UCP Merchant Server in one terminal:

```shell
uv run --with ucp-sdk --with fastapi --with uvicorn python server.py
```

You can inspect the discovery endpoint directly with `curl`:

```shell
curl -s http://127.0.0.1:8182/.well-known/ucp | jq .
```

Then run the UCP Client against the live server in a second terminal:

```shell
uv run --with ucp-sdk --with fastapi --with httpx python client.py --server_url http://127.0.0.1:8182
```

## Expected output

```text
=== 1. UCP Discovery (GET /.well-known/ucp) ===
Protocol Version:  2026-08-25
Services:          ['dev.ucp.shopping']
Capabilities:      ['dev.ucp.shopping.checkout', 'dev.ucp.shopping.fulfillment', 'dev.ucp.shopping.discount']
Payment Handlers:  ['com.google.pay', 'dev.shopify.shop_pay']
Signing Key (kid): merchant_key_2026

=== 2. Create Checkout Session (POST /checkout-sessions) ===
Checkout ID:       chk_9c35e04f
Checkout Status:   incomplete
Negotiated Caps:   ['dev.ucp.shopping.checkout', 'dev.ucp.shopping.fulfillment', 'dev.ucp.shopping.discount']
  - 1x Red Roses Bouquet (sku_roses): $25.00
  - 1x Ceramic Vase (sku_vase): $15.00

=== 3. Update Checkout: Fulfillment & Discount (PUT /checkout-sessions/chk_9c35e04f) ===
Checkout Status:   ready_for_complete
Totals Breakdown:
  - Subtotal                : $40.00
  - 10% Promo (SAVE10)      : -$4.00
  - Shipping (Express Delivery): $5.00
  - Total                   : $41.00

=== 4. Complete Checkout (POST /checkout-sessions/chk_9c35e04f/complete) ===
Checkout Status:   completed
Order Created:     Order #ORD_EF9FCC12 (id=ord_ef9fcc12)
Order Permalink:   https://flowershop.example.com/orders/ord_ef9fcc12
```
