# UCP with Agent Development Kit (ADK)

An example showing how a Google ADK agent ([`shopping_agent`](./shopping_agent/agent.py)) uses the **Universal Commerce Protocol (UCP)** and `ucp-sdk` to discover a merchant's capabilities via `/.well-known/ucp`, negotiate checkout extensions (`fulfillment`, `discount`), and complete an order.

## Setup

Create and activate a virtual environment and install dependencies:

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `dotenv` to `.env` inside `shopping_agent/` (or the current directory) and set your Gemini API key or Vertex AI project:

```shell
cp dotenv .env
```

## 1. Start the UCP Merchant Server

In your first terminal, start the local UCP Merchant Server from [`../hello-world/server.py`](../hello-world/server.py) on port `8182`:

```shell
python ../hello-world/server.py
```

## 2. Run the ADK Shopping Agent

In a second terminal (inside `samples/protocols/ucp/adk/`), launch the ADK Web UI:

```shell
adk web
```

Open `http://127.0.0.1:8000` in your browser, select `shopping_agent`, and try prompts through the UCP lifecycle:

```text
[user]: What capabilities and products does this merchant support?

[ucp_shopping_agent]: I checked the merchant's UCP profile at /.well-known/ucp (version 2026-08-25):
- Capabilities: dev.ucp.shopping.checkout, dev.ucp.shopping.fulfillment, dev.ucp.shopping.discount
- Payment Handlers: com.google.pay, dev.shopify.shop_pay
- Products:
  * Red Roses Bouquet (sku_roses) - $25.00
  * Ceramic Vase (sku_vase) - $15.00
```

```text
[user]: Buy 1 Red Roses Bouquet with Express Delivery, promo code SAVE10, email alice@example.com, and pay with Google Pay.

[ucp_shopping_agent]: Your order is complete!
- Checkout ID: chk_a1b2c3d4 (status: completed)
- Subtotal: $25.00 | Discount (SAVE10): -$2.50 | Express Delivery: $5.00 | Total: $27.50
- Order: Order #ORD_9F8E7D6C
- Permalink: https://flowershop.example.com/orders/ord_9f8e7d6c
```
