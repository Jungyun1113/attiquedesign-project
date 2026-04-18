import math
from chalice import Blueprint
from sqlmodel import select

from chalicelib.core.db import get_session
from chalicelib.core.auth import require_admin
from chalicelib.core.exceptions import success_response, handle_app_error, AppError, ValidationError
from chalicelib.helpers.db import fetch, bulk_fetch, insert, update, delete
from chalicelib.models.product import Product, ProductImage, ProductStatus

products_bp = Blueprint(__name__)

_SORT_FIELDS = {
    "created_at": Product.created_at,
    "price": Product.price,
    "name": Product.name,
}


def _serialize_product(session, p: Product) -> dict:
    images_stmt = (
        select(ProductImage)
        .where(ProductImage.product_id == p.id)
        .where(ProductImage.is_deleted == False)
        .order_by(ProductImage.display_order)
    )
    images = session.exec(images_stmt).all()
    return {
        "id": str(p.id),
        "sku": p.sku,
        "name": p.name,
        "category": p.category,
        "price": float(p.price) if p.price is not None else None,
        "stock_quantity": p.stock_quantity,
        "status": p.status.value,
        "thumbnail_url": p.thumbnail_url,
        "images": [
            {
                "id": str(img.id),
                "image_url": img.image_url,
                "display_order": img.display_order,
                "is_primary": img.is_primary,
            }
            for img in images
        ],
    }


@products_bp.route("/products", methods=["GET"], cors=True)
def list_products():
    try:
        params = products_bp.current_request.query_params or {}
        page = int(params.get("page", 1))
        size = min(int(params.get("limit", 20)), 100)
        category = params.get("category")
        status = params.get("status")
        sort = params.get("sort", "created_at")
        order = params.get("order", "desc")

        filters = {}
        if category:
            filters["category"] = category
        if status:
            try:
                filters["status"] = ProductStatus(status)
            except ValueError:
                raise ValidationError(f"유효하지 않은 status: {status}")

        sort_col = _SORT_FIELDS.get(sort, Product.created_at)
        order_by = sort_col.asc() if order == "asc" else sort_col.desc()

        with get_session() as session:
            items, total = bulk_fetch(
                session, Product, filters=filters, order_by=order_by, page=page, size=size
            )
            result = [_serialize_product(session, p) for p in items]

        total_pages = math.ceil(total / size) if size else 1
        return success_response(
            result,
            meta={"page": page, "size": size, "total_count": total, "total_pages": total_pages},
        )
    except AppError as e:
        return handle_app_error(e)


@products_bp.route("/products/{product_id}", methods=["GET"], cors=True)
def get_product(product_id):
    try:
        with get_session() as session:
            product = fetch(session, Product, raise_not_found=True, id=product_id)
            result = _serialize_product(session, product)
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@products_bp.route("/products", methods=["POST"], cors=True)
@require_admin
def create_product():
    try:
        body = products_bp.current_request.json_body or {}
        required = ["sku", "name", "category"]
        missing = [f for f in required if not body.get(f)]
        if missing:
            raise ValidationError(f"필수 필드 누락: {', '.join(missing)}")

        with get_session() as session:
            product = insert(session, Product, {
                "sku": body["sku"],
                "name": body["name"],
                "category": body["category"],
                "price": body.get("price"),
                "stock_quantity": body.get("stock_quantity", 0),
                "status": body.get("status", "ACTIVE"),
                "thumbnail_url": body.get("thumbnail_url"),
            })
            result = _serialize_product(session, product)
        return success_response(result, status_code=201)
    except AppError as e:
        return handle_app_error(e)


@products_bp.route("/products/{product_id}", methods=["PATCH"], cors=True)
@require_admin
def patch_product(product_id):
    try:
        body = products_bp.current_request.json_body or {}
        allowed = {"name", "category", "price", "stock_quantity", "status", "thumbnail_url"}
        data = {k: v for k, v in body.items() if k in allowed}

        with get_session() as session:
            product = fetch(session, Product, raise_not_found=True, id=product_id)
            product = update(session, product, data)
            result = _serialize_product(session, product)
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@products_bp.route("/products/{product_id}", methods=["DELETE"], cors=True)
@require_admin
def delete_product(product_id):
    try:
        with get_session() as session:
            product = fetch(session, Product, raise_not_found=True, id=product_id)
            delete(session, product)
        return success_response({"message": "삭제되었습니다."})
    except AppError as e:
        return handle_app_error(e)
