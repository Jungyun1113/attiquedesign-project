import math
from datetime import datetime

from chalice import Blueprint

from chalicelib.core.db import get_session
from chalicelib.core.auth import require_admin, try_extract_user
from chalicelib.core.context import get_user_id
from chalicelib.core.exceptions import success_response, handle_app_error, AppError, ValidationError
from chalicelib.helpers.db import fetch, bulk_fetch, insert, update
from chalicelib.models.reservation import Reservation, ReservationType, ReservationStatus

reservations_bp = Blueprint(__name__)


def _serialize_reservation(r: Reservation) -> dict:
    return {
        "id": str(r.id),
        "user_id": str(r.user_id) if r.user_id else None,
        "reservation_type": r.reservation_type.value,
        "status": r.status.value,
        "expected_date": r.expected_date.isoformat() if r.expected_date else None,
        "guest_info": r.guest_info,
        "dynamic_data": r.dynamic_data,
        "created_at": r.created_at.isoformat(),
    }


@reservations_bp.route("/reservations", methods=["POST"], cors=True)
def create_reservation():
    """예약 생성. 비회원/회원 모두 허용."""
    try:
        body = reservations_bp.current_request.json_body or {}
        request = reservations_bp.current_request

        reservation_type = body.get("reservation_type")
        if not reservation_type:
            raise ValidationError("reservation_type은 필수입니다.")

        try:
            rtype = ReservationType(reservation_type)
        except ValueError:
            raise ValidationError(f"유효하지 않은 예약 유형: {reservation_type}")

        expected_date = None
        raw_date = body.get("expected_date")
        if raw_date:
            try:
                expected_date = datetime.fromisoformat(raw_date)
            except ValueError:
                raise ValidationError("expected_date 형식이 올바르지 않습니다. (ISO 8601)")

        # 토큰이 있으면 회원으로, 없으면 비회원으로 처리
        user_id = try_extract_user(request)

        with get_session() as session:
            reservation = insert(session, Reservation, {
                "user_id": user_id,
                "reservation_type": rtype,
                "expected_date": expected_date,
                "guest_info": body.get("guest_info"),
                "dynamic_data": body.get("dynamic_data"),
                "status": ReservationStatus.RECEIVED,
            })

        return success_response(_serialize_reservation(reservation), status_code=201)
    except AppError as e:
        return handle_app_error(e)


@reservations_bp.route("/reservations", methods=["GET"], cors=True)
@require_admin
def list_reservations():
    """관리자: 예약 목록 (CRM 대시보드)."""
    try:
        params = reservations_bp.current_request.query_params or {}
        page = int(params.get("page", 1))
        size = min(int(params.get("limit", 20)), 100)
        status_filter = params.get("status")
        type_filter = params.get("type")

        filters = {}
        if status_filter:
            try:
                filters["status"] = ReservationStatus(status_filter)
            except ValueError:
                raise ValidationError(f"유효하지 않은 status: {status_filter}")
        if type_filter:
            try:
                filters["reservation_type"] = ReservationType(type_filter)
            except ValueError:
                raise ValidationError(f"유효하지 않은 type: {type_filter}")

        with get_session() as session:
            items, total = bulk_fetch(session, Reservation, filters=filters, page=page, size=size)

        total_pages = math.ceil(total / size) if size else 1
        return success_response(
            [_serialize_reservation(r) for r in items],
            meta={"page": page, "size": size, "total_count": total, "total_pages": total_pages},
        )
    except AppError as e:
        return handle_app_error(e)


@reservations_bp.route("/reservations/{reservation_id}/status", methods=["PATCH"], cors=True)
@require_admin
def update_reservation_status(reservation_id):
    """관리자: 예약 상태 변경."""
    try:
        body = reservations_bp.current_request.json_body or {}
        status_value = body.get("status")
        if not status_value:
            raise ValidationError("status는 필수입니다.")

        try:
            new_status = ReservationStatus(status_value)
        except ValueError:
            raise ValidationError(f"유효하지 않은 상태: {status_value}")

        with get_session() as session:
            reservation = fetch(session, Reservation, raise_not_found=True, id=reservation_id)
            reservation = update(session, reservation, {"status": new_status})

        return success_response(_serialize_reservation(reservation))
    except AppError as e:
        return handle_app_error(e)
