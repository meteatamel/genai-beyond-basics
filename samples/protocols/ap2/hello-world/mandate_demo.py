"""Hello World demo of the Agent Payments Protocol (AP2) using the official AP2 Python SDK.

Walks through an autonomous (Human Not Present) shopping flow:
1. Trusted Surface (User) signs Open Checkout & Payment Mandates with constraints (SD-JWT).
2. Merchant creates a signed UCP Checkout JWT for an item in stock.
3. Shopping Agent autonomously signs Closed Checkout & Payment Mandates (KB-SD-JWT chain).
4. Merchant & Credential Provider deterministically verify the mandate chains and issue Receipts.
5. Demonstrates how AP2 catches constraint violations (e.g. an agent exceeding the budget).
"""

import json
import time

from ap2.sdk.checkout_mandate_chain import CheckoutMandateChain
from ap2.sdk.generated.checkout_mandate import CheckoutMandate
from ap2.sdk.generated.open_checkout_mandate import (
    AllowedMerchants,
    Item as MandateItem,
    LineItemRequirements,
    LineItems,
    OpenCheckoutMandate,
)
from ap2.sdk.generated.open_payment_mandate import (
    AllowedPayees,
    AmountRange,
    OpenPaymentMandate,
)
from ap2.sdk.generated.payment_mandate import PaymentMandate
from ap2.sdk.generated.types.amount import Amount
from ap2.sdk.generated.types.checkout import Checkout, Status
from ap2.sdk.generated.types.item import Item
from ap2.sdk.generated.types.line_item import LineItem
from ap2.sdk.generated.types.link import Link
from ap2.sdk.generated.types.merchant import Merchant
from ap2.sdk.generated.types.payment_instrument import PaymentInstrument
from ap2.sdk.generated.types.total import Total
from ap2.sdk.jwt_helper import create_jwt
from ap2.sdk.mandate import MandateClient
from ap2.sdk.payment_mandate_chain import PaymentMandateChain
from ap2.sdk.receipt_wrapper import ReceiptClient
from ap2.sdk.utils import compute_sha256_b64url
from cryptography.hazmat.primitives.asymmetric import ec
from jwcrypto.jwk import JWK


def generate_jwk(kid: str) -> JWK:
    """Generate an ES256 (P-256) JWK key pair with a key ID."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    jwk_dict = json.loads(JWK.from_pyca(private_key).export())
    jwk_dict["kid"] = kid
    return JWK(**jwk_dict)


def main() -> None:
    print("=== 1. Generating Keys for User (Trusted Surface), Agent, and Merchant ===")
    user_jwk = generate_jwk("user-key-1")
    user_pub_jwk = JWK.from_json(user_jwk.export_public())

    agent_jwk = generate_jwk("shopping-agent-key-1")
    agent_pub_dict = json.loads(agent_jwk.export_public())

    merchant_jwk = generate_jwk("merchant-key-1")
    merchant_pub_jwk = JWK.from_json(merchant_jwk.export_public())

    psp_jwk = generate_jwk("psp-key-1")
    psp_pub_jwk = JWK.from_json(psp_jwk.export_public())

    client = MandateClient()
    receipt_client = ReceiptClient()
    now = int(time.time())

    merchant = Merchant(
        id="merchant_shoes_1",
        name="RunFast Store",
        website="https://runfast.example.com",
    )
    card_instrument = PaymentInstrument(
        id="card_visa_4242",
        type="card",
        description="Visa •••• 4242",
    )

    print("\n=== 2. User Signs Open Mandates on Trusted Surface (SD-JWT) ===")
    print("Intent: 'Buy white running shoes (SKU-SHOE-WHITE) from RunFast Store for at most $150.00'")

    # Open Checkout Mandate: constrains WHO the agent can buy from and WHAT items
    open_checkout_token = client.create(
        payloads=[
            OpenCheckoutMandate(
                constraints=[
                    AllowedMerchants(allowed=[merchant]),
                    LineItems(
                        items=[
                            LineItemRequirements(
                                id="req-running-shoes",
                                acceptable_items=[
                                    MandateItem(
                                        id="SKU-SHOE-WHITE",
                                        title="CloudRunner White Shoes",
                                    )
                                ],
                                quantity=1,
                            )
                        ]
                    ),
                ],
                cnf={"jwk": agent_pub_dict},  # Binds mandate to Shopping Agent's public key
                iat=now,
                exp=now + 3600,
            )
        ],
        issuer_key=user_jwk,
    )

    # Open Payment Mandate: constrains HOW MUCH the agent can spend ($150.00 = 15000 cents)
    open_payment_token = client.create(
        payloads=[
            OpenPaymentMandate(
                constraints=[
                    AmountRange(currency="USD", min=0, max=15000),
                    AllowedPayees(allowed=[merchant]),
                ],
                cnf={"jwk": agent_pub_dict},
                iat=now,
                exp=now + 3600,
            )
        ],
        issuer_key=user_jwk,
    )
    print(f"Open Checkout Mandate (SD-JWT): {open_checkout_token[:65]}...")
    print(f"Open Payment Mandate  (SD-JWT): {open_payment_token[:65]}...")

    print("\n=== 3. Merchant Creates Signed UCP Checkout ($120.00) ===")
    unit_price_cents = 12000  # $120.00
    checkout = Checkout(
        id="chk_98765",
        merchant=merchant,
        line_items=[
            LineItem(
                id="li_1",
                item=Item(
                    id="SKU-SHOE-WHITE",
                    title="CloudRunner White Shoes",
                    price=unit_price_cents,
                ),
                quantity=1,
                totals=[
                    Total(type="subtotal", amount=unit_price_cents),
                    Total(type="total", amount=unit_price_cents),
                ],
            )
        ],
        status=Status.ready_for_complete,
        currency="USD",
        totals=[
            Total(type="subtotal", amount=unit_price_cents),
            Total(type="total", amount=unit_price_cents),
        ],
        links=[
            Link(type="terms_of_service", url="https://runfast.example.com/tos"),
        ],
    )
    checkout_jwt = create_jwt(
        header={"alg": "ES256", "typ": "JWT", "kid": "merchant-key-1"},
        payload=json.loads(checkout.model_dump_json(exclude_none=True)),
        private_key=merchant_jwk,
    )
    checkout_hash = compute_sha256_b64url(checkout_jwt)
    print(f"Merchant Checkout JWT Hash: {checkout_hash}")

    print("\n=== 4. Shopping Agent Signs Closed Mandates (KB-SD-JWT Delegation Chain) ===")
    checkout_chain_token = client.present(
        holder_key=agent_jwk,
        mandate_token=open_checkout_token,
        payloads=[
            CheckoutMandate(
                checkout_jwt=checkout_jwt,
                checkout_hash=checkout_hash,
                iat=now,
                exp=now + 3600,
            )
        ],
        aud="merchant",
        nonce="nonce_chk_98765",
    )

    closed_payment = PaymentMandate(
        transaction_id=checkout_hash,
        payee=merchant,
        payment_amount=Amount(amount=unit_price_cents, currency="USD"),
        payment_instrument=card_instrument,
        iat=now,
        exp=now + 3600,
    )
    payment_chain_token = client.present(
        holder_key=agent_jwk,
        mandate_token=open_payment_token,
        payloads=[closed_payment],
        aud="credential-provider",
        nonce="nonce_pay_98765",
    )
    print("Agent appended closed KB-SD-JWT hop to both open mandates.")

    print("\n=== 5. Deterministic Verification & Receipt Issuance ===")
    # 5a. Merchant verifies Checkout Mandate Chain
    checkout_payloads = client.verify(
        token=checkout_chain_token,
        key_or_provider=lambda _tok: user_pub_jwk,
        expected_aud="merchant",
        expected_nonce="nonce_chk_98765",
    )
    checkout_chain = CheckoutMandateChain.parse(checkout_payloads)
    checkout_violations = checkout_chain.verify(
        expected_checkout_hash=checkout_hash,
        checkout_jwt=checkout_jwt,
    )
    assert not checkout_violations, f"Unexpected violations: {checkout_violations}"
    print("[Merchant] Checkout Mandate Chain verified! Constraints satisfied (0 violations).")

    # 5b. Credential Provider / Payment Processor verifies Payment Mandate Chain
    payment_payloads = client.verify(
        token=payment_chain_token,
        key_or_provider=lambda _tok: user_pub_jwk,
        expected_aud="credential-provider",
        expected_nonce="nonce_pay_98765",
    )
    payment_chain = PaymentMandateChain.parse(payment_payloads)
    payment_violations = payment_chain.verify(expected_transaction_id=checkout_hash)
    assert not payment_violations, f"Unexpected violations: {payment_violations}"
    print("[Payment Processor] Payment Mandate Chain verified! Amount $120.00 <= $150.00 max.")

    # 5c. Issue and verify Receipts bound to the closed leaf JWT hashes
    checkout_ref = compute_sha256_b64url(client.get_closed_mandate_jwt(checkout_chain_token))
    checkout_receipt = receipt_client.create_checkout_receipt(
        merchant=merchant.website,
        reference=checkout_ref,
        order_id="ord_1001",
    )
    checkout_receipt_jwt = create_jwt(
        header={"alg": "ES256", "typ": "JWT"},
        payload=json.loads(checkout_receipt.model_dump_json(exclude_none=True)),
        private_key=merchant_jwk,
    )
    chk_receipt_result = receipt_client.verify_receipt(
        receipt_jwt=checkout_receipt_jwt,
        receipt_issuer_public_key=merchant_pub_jwk,
        has_reference_in_store_cb=lambda ref: ref == checkout_ref,
        is_payment_receipt=False,
    )
    print(f"[Shopping Agent] Checkout Receipt verified: {chk_receipt_result}")

    payment_ref = compute_sha256_b64url(client.get_closed_mandate_jwt(payment_chain_token))
    payment_receipt = receipt_client.create_payment_receipt(
        payment_mandate_content=closed_payment,
        reference=payment_ref,
    )
    payment_receipt_jwt = create_jwt(
        header={"alg": "ES256", "typ": "JWT"},
        payload=json.loads(payment_receipt.model_dump_json(exclude_none=True)),
        private_key=psp_jwk,
    )
    pay_receipt_result = receipt_client.verify_receipt(
        receipt_jwt=payment_receipt_jwt,
        receipt_issuer_public_key=psp_pub_jwk,
        has_reference_in_store_cb=lambda ref: ref == payment_ref,
        is_payment_receipt=True,
    )
    print(f"[Shopping Agent] Payment Receipt verified:  {pay_receipt_result}")

    print("\n=== 6. Guardrail Demo: Agent Tries to Exceed Budget ($250.00 > $150.00) ===")
    over_budget_chain_token = client.present(
        holder_key=agent_jwk,
        mandate_token=open_payment_token,
        payloads=[
            PaymentMandate(
                transaction_id="tx_over_budget",
                payee=merchant,
                payment_amount=Amount(amount=25000, currency="USD"),  # $250.00!
                payment_instrument=card_instrument,
                iat=now,
                exp=now + 3600,
            )
        ],
        aud="credential-provider",
        nonce="nonce_over_budget",
    )
    over_budget_payloads = client.verify(
        token=over_budget_chain_token,
        key_or_provider=lambda _tok: user_pub_jwk,
        expected_aud="credential-provider",
        expected_nonce="nonce_over_budget",
    )
    over_budget_chain = PaymentMandateChain.parse(over_budget_payloads)
    violations = over_budget_chain.verify(expected_transaction_id="tx_over_budget")
    print(f"[Payment Processor] Rejected over-budget payment! Violations: {violations}")


if __name__ == "__main__":
    main()
