from chalice import Blueprint

from chalicelib.core.db import get_session
from chalicelib.core.config import settings
from chalicelib.core.exceptions import (
    success_response, handle_app_error, AppError,
    ValidationError, UnauthorizedError,
)
from chalicelib.helpers.db import fetch, update
from chalicelib.models.order import Order, OrderStatus
from chalicelib.services.payment_service import verify_payment_amount, verify_webhook_signature

webhooks_bp = Blueprint(__name__)


@webhooks_bp.route("/webhooks/payments", methods=["POST"], cors=True)
def payment_webhook():
    try:
        request = webhooks_bp.current_request

        # HMAC 서명 검증 (PORTONE_WEBHOOK_SECRET가 설정된 경우만 강제 검증)
        if settings.PORTONE_WEBHOOK_SECRET:
            signature = request.headers.get("webhook-signature", "")
            raw_body = request.raw_body if hasattr(request, "raw_body") else b""
            if raw_body and not verify_webhook_signature(raw_body, signature):
                raise UnauthorizedError("웹훅 서명이 유효하지 않습니다.")

        body = request.json_body or {}

        payment_id = body.get("paymentId") or body.get("payment_id")
        order_id = body.get("orderId") or body.get("order_id")
        status = body.get("status")

        if not payment_id or not order_id:
            raise ValidationError("paymentId와 orderId는 필수입니다.")

        with get_session() as session:
            order = fetch(session, Order, raise_not_found=True, id=order_id)

            if status == "PAID":
                is_valid = verify_payment_amount(payment_id, order.total_amount)
                if not is_valid:
                    update(session, order, {"status": OrderStatus.CANCELLED})
                    raise ValidationError("결제 금액이 일치하지 않습니다.")

                update(session, order, {
                    "status": OrderStatus.PAID,
                    "pg_transaction_id": payment_id,
                })
            elif status in ("CANCELLED", "FAILED"):
                update(session, order, {"status": OrderStatus.CANCELLED})

        return success_response({"message": "처리 완료"})
    except AppError as e:
        return handle_app_error(e)
