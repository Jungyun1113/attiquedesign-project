import hmac
import hashlib
import httpx
from decimal import Decimal

from chalicelib.core.config import settings
from chalicelib.core.exceptions import ValidationError


PORTONE_API_BASE = "https://api.portone.io"


def verify_webhook_signature(raw_body: bytes, signature_header: str) -> bool:
    expected = hmac.new(
        key=settings.PORTONE_WEBHOOK_SECRET.encode(),
        msg=raw_body,
        digestmod=hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


def get_payment(payment_id: str) -> dict:
    headers = {"Authorization": f"PortOne {settings.PORTONE_API_SECRET}"}
    response = httpx.get(
        f"{PORTONE_API_BASE}/payments/{payment_id}",
        headers=headers,
        timeout=10,
    )
    if response.status_code != 200:
        raise ValidationError("결제 정보를 가져올 수 없습니다.")
    return response.json()


def verify_payment_amount(payment_id: str, expected_amount: Decimal) -> bool:
    payment = get_payment(payment_id)
    paid_amount = Decimal(str(payment.get("amount", {}).get("total", 0)))
    status = payment.get("status", "")
    return status == "PAID" and paid_amount == expected_amount
