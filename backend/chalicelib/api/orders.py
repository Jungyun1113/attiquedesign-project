import math
from decimal import Decimal
from chalice import Blueprint
from sqlmodel import select

from chalicelib.core.db import get_session
from chalicelib.core.auth import require_auth, require_admin, try_extract_user
from chalicelib.core.context import get_user_id
from chalicelib.core.exceptions import (
    success_response, handle_app_error, AppError,
    NotFoundError, ForbiddenError, ValidationError,
)
from chalicelib.helpers.db import fetch, bulk_fetch, insert, update
from chalicelib.models.order import Order, OrderItem, OrderStatus
from chalicelib.models.product import Product

orders_bp = Blueprint(__name__)


def _serialize_order(session, order: Order) -> dict:
    items_stmt = (
        select(OrderItem)
        .where(OrderItem.order_id == order.id)
        .where(OrderItem.is_deleted == False)
    )
    items = session.exec(items_stmt).all()

    product_ids = [i.product_id for i in items]
    products_map: dict = {}
    if product_ids:
        products_stmt = select(Product).where(Product.id.in_(product_ids))
        products_map = {p.id: p for p in session.exec(products_stmt).all()}

    return {
        "id": str(order.id),
        "user_id": str(order.user_id) if order.user_id else None,
        "guest_email": order.guest_email,
        "guest_name": order.guest_name,
        "guest_phone": order.guest_phone,
        "total_amount": float(order.total_amount),
        "status": order.status.value,
        "pg_transaction_id": order.pg_transaction_id,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "id": str(i.id),
                "product_id": str(i.product_id),
                "product_name": products_map[i.product_id].name if i.product_id in products_map else None,
                "quantity": i.quantity,
                "unit_price": float(i.unit_price),
            }
            for i in items
        ],
    }


@orders_bp.route("/orders", methods=["POST"], cors=True)
def create_order():
    """주문 생성. JWT가 있으면 회원 주문, 없으면 비회원 주문으로 처리."""
    try:
        request = orders_bp.current_request
        body = request.json_body or {}
        items_data = body.get("items", [])

        if not items_data:
            raise ValidationError("주문 항목이 없습니다.")

        # 토큰이 있으면 회원 주문으로 처리 (없어도 비회원 주문 허용)
        user_id = try_extract_user(request)

        with get_session() as session:
            total_amount = Decimal("0")
            order_items_payload = []

            for item in items_data:
                product = fetch(session, Product, raise_not_found=True, id=item["product_id"])
                qty = int(item["quantity"])
                if product.stock_quantity < qty:
                    raise ValidationError(f"'{product.name}' 재고가 부족합니다.")

                unit_price = Decimal(str(item["unit_price"]))
                total_amount += unit_price * qty
                order_items_payload.append({
                    "product_id": product.id,
                    "quantity": qty,
                    "unit_price": unit_price,
                })
                product.stock_quantity -= qty
                session.add(product)

            order = insert(session, Order, {
                "user_id": user_id,
                "guest_email": body.get("guest_email"),
                "guest_phone": body.get("guest_phone"),
                "guest_name": body.get("guest_name"),
                "total_amount": total_amount,
                "status": OrderStatus.PENDING,
            })

            for item_payload in order_items_payload:
                item_payload["order_id"] = order.id
                insert(session, OrderItem, item_payload)

            result = _serialize_order(session, order)

        return success_response(result, status_code=201)
    except AppError as e:
        return handle_app_error(e)


@orders_bp.route("/orders/me", methods=["GET"], cors=True)
@require_auth
def list_my_orders():
    try:
        user_id = get_user_id()
        params = orders_bp.current_request.query_params or {}
        page = int(params.get("page", 1))
        size = min(int(params.get("limit", 20)), 100)

        with get_session() as session:
            items, total = bulk_fetch(
                session, Order,
                filters={"user_id": user_id},
                page=page, size=size,
            )
            result = [_serialize_order(session, o) for o in items]

        total_pages = math.ceil(total / size) if size else 1
        return success_response(
            result,
            meta={"page": page, "size": size, "total_count": total, "total_pages": total_pages},
        )
    except AppError as e:
        return handle_app_error(e)


@orders_bp.route("/orders/{order_id}", methods=["GET"], cors=True)
def get_order(order_id):
    try:
        request = orders_bp.current_request
        caller_user_id = try_extract_user(request)

        with get_session() as session:
            order = fetch(session, Order, raise_not_found=True, id=order_id)

            # 회원 주문: 본인만 조회 가능
            if order.user_id and str(order.user_id) != str(caller_user_id):
                raise ForbiddenError()

            result = _serialize_order(session, order)

        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@orders_bp.route("/orders", methods=["GET"], cors=True)
@require_admin
def list_all_orders():
    """관리자: 전체 주문 목록 조회."""
    try:
        params = orders_bp.current_request.query_params or {}
        page = int(params.get("page", 1))
        size = min(int(params.get("limit", 20)), 100)
        status_filter = params.get("status")

        filters = {}
        if status_filter:
            try:
                filters["status"] = OrderStatus(status_filter)
            except ValueError:
                raise ValidationError(f"유효하지 않은 status: {status_filter}")

        with get_session() as session:
            items, total = bulk_fetch(
                session, Order, filters=filters, page=page, size=size
            )
            result = [_serialize_order(session, o) for o in items]

        total_pages = math.ceil(total / size) if size else 1
        return success_response(
            result,
            meta={"page": page, "size": size, "total_count": total, "total_pages": total_pages},
        )
    except AppError as e:
        return handle_app_error(e)


@orders_bp.route("/orders/{order_id}/status", methods=["PATCH"], cors=True)
@require_admin
def update_order_status(order_id):
    """관리자: 주문 상태 변경."""
    try:
        body = orders_bp.current_request.json_body or {}
        status_value = body.get("status")
        if not status_value:
            raise ValidationError("status는 필수입니다.")

        try:
            new_status = OrderStatus(status_value)
        except ValueError:
            raise ValidationError(f"유효하지 않은 status: {status_value}")

        with get_session() as session:
            order = fetch(session, Order, raise_not_found=True, id=order_id)
            order = update(session, order, {"status": new_status})
            result = _serialize_order(session, order)

        return success_response(result)
    except AppError as e:
        return handle_app_error(e)
