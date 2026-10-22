# AP2 Hello World (Python SDK)

A minimal, self-contained "Hello World" sample using the official [AP2 Python SDK](https://github.com/google-agentic-commerce/AP2/tree/main/code/sdk/python/ap2/sdk) (`ap2.sdk`).

Without needing to spin up multiple servers or configure API keys, [mandate_demo.py](./mandate_demo.py) walks through an end-to-end **Autonomous (Human Not Present)** AP2 transaction in a single script:

1. **Key Generation**: Generates ES256 (`P-256`) JWK keys for the **User (Trusted Surface)**, **Shopping Agent**, **Merchant**, and **Payment Processor**.
2. **Open Mandates (`SD-JWT`)**: The User approves an `OpenCheckoutMandate` (constraining allowed merchants and acceptable SKUs) and an `OpenPaymentMandate` (constraining maximum spend to `$150.00`), both cryptographically bound to the Shopping Agent's public key via the `cnf` claim.
3. **Merchant Checkout JWT**: The Merchant creates and signs a UCP-compatible `Checkout` JWT for `CloudRunner White Shoes` (`SKU-SHOE-WHITE`) priced at `$120.00`.
4. **Closed Mandates (`KB-SD-JWT` Delegation Chain)**: Acting autonomously, the Shopping Agent signs a closed `CheckoutMandate` (bound to the `checkout_hash`) and a closed `PaymentMandate` on top of the user's open mandates using `MandateClient.present()`.
5. **Deterministic Verification & Receipts**:
   * The Merchant verifies the `CheckoutMandateChain` (`MandateClient.verify()` + `CheckoutMandateChain.parse().verify()`) and issues a signed `CheckoutReceipt`.
   * The Payment Processor verifies the `PaymentMandateChain` (`PaymentMandateChain.parse().verify()`) and issues a signed `PaymentReceipt`.
6. **Constraint Guardrail Check**: Demonstrates what happens when the agent attempts to pay `$250.00` against the `$150.00` open mandate—deterministic verification immediately rejects the transaction (`Amount 25000 exceeds maximum 15000`).

## Run the sample

### Option 1: Run directly with `uv`

```shell
uv run --with "ap2 @ git+https://github.com/google-agentic-commerce/AP2.git" python mandate_demo.py
```

### Option 2: Run with `venv` and `pip`

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python mandate_demo.py
```

## Expected output

```text
=== 1. Generating Keys for User (Trusted Surface), Agent, and Merchant ===

=== 2. User Signs Open Mandates on Trusted Surface (SD-JWT) ===
Intent: 'Buy white running shoes (SKU-SHOE-WHITE) from RunFast Store for at most $150.00'
Open Checkout Mandate (SD-JWT): eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0IiwgImtpZCI6I...
Open Payment Mandate  (SD-JWT): eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0IiwgImtpZCI6I...

=== 3. Merchant Creates Signed UCP Checkout ($120.00) ===
Merchant Checkout JWT Hash: MBOOU7B8tmrp1fickmNKbaLJ74iQRtvSnO2HQ01ILU0

=== 4. Shopping Agent Signs Closed Mandates (KB-SD-JWT Delegation Chain) ===
Agent appended closed KB-SD-JWT hop to both open mandates.

=== 5. Deterministic Verification & Receipt Issuance ===
[Merchant] Checkout Mandate Chain verified! Constraints satisfied (0 violations).
[Payment Processor] Payment Mandate Chain verified! Amount $120.00 <= $150.00 max.
[Shopping Agent] Checkout Receipt verified: {'verified': True}
[Shopping Agent] Payment Receipt verified:  {'verified': True}

=== 6. Guardrail Demo: Agent Tries to Exceed Budget ($250.00 > $150.00) ===
[Payment Processor] Rejected over-budget payment! Violations: ['Amount 25000 exceeds maximum 15000']
```
