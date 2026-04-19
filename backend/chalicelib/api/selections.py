import math
from chalice import Blueprint
from sqlmodel import select

from chalicelib.core.db import get_session
from chalicelib.core.auth import require_admin
from chalicelib.core.exceptions import success_response, handle_app_error, AppError, NotFoundError, ValidationError
from chalicelib.helpers.db import fetch, bulk_fetch, insert, update, delete
from chalicelib.models.selection import Selection, SelectionImage, SelectionProduct
from chalicelib.models.product import Product
from chalicelib.services.storage_service import get_image_display_url

selections_bp = Blueprint(__name__)


def _serialize_selection_products(session, selection_id) -> list:
    sp_stmt = (
        select(SelectionProduct)
        .where(SelectionProduct.selection_id == selection_id)
        .where(SelectionProduct.is_deleted == False)
        .order_by(SelectionProduct.display_order)
    )
    sps = session.exec(sp_stmt).all()

    if not sps:
        return []

    product_ids = [sp.product_id for sp in sps]
    products_stmt = (
        select(Product)
        .where(Product.id.in_(product_ids))
        .where(Product.is_deleted == False)
    )
    products_map = {p.id: p for p in session.exec(products_stmt).all()}

    return [
        {
            "id": str(sp.id),
            "product_id": str(sp.product_id),
            "display_order": sp.display_order,
            "name": products_map[sp.product_id].name if sp.product_id in products_map else None,
            "thumbnail_url": products_map[sp.product_id].thumbnail_url if sp.product_id in products_map else None,
            "price": float(products_map[sp.product_id].price) if sp.product_id in products_map and products_map[sp.product_id].price else None,
            "status": products_map[sp.product_id].status.value if sp.product_id in products_map else None,
        }
        for sp in sps
    ]


def _serialize_selection_images(session, selection_id) -> list:
    img_stmt = (
        select(SelectionImage)
        .where(SelectionImage.selection_id == selection_id)
        .where(SelectionImage.is_deleted == False)
        .order_by(SelectionImage.display_order)
    )
    images = session.exec(img_stmt).all()
    return [
        {
            "id": str(img.id),
            "image_url": get_image_display_url(img.image_url),
            "display_order": img.display_order,
        }
        for img in images
    ]


def _serialize_selection(session, s: Selection) -> dict:
    return {
        "id": str(s.id),
        "title": s.title,
        "subtitle": s.subtitle,
        "description": s.description,
        "images": _serialize_selection_images(session, s.id),
        "products": _serialize_selection_products(session, s.id),
    }


@selections_bp.route("/selections", methods=["GET"], cors=True)
def list_selections():
    try:
        params = selections_bp.current_request.query_params or {}
        page = int(params.get("page", 1))
        size = min(int(params.get("limit", 20)), 100)

        with get_session() as session:
            items, total = bulk_fetch(session, Selection, page=page, size=size)

            # Batch fetch images and products in 2 queries instead of N*2
            selection_ids = [s.id for s in items]
            images_by_selection: dict = {}
            products_by_selection: dict = {}

            if selection_ids:
                imgs_stmt = (
                    select(SelectionImage)
                    .where(SelectionImage.selection_id.in_(selection_ids))
                    .where(SelectionImage.is_deleted == False)
                    .order_by(SelectionImage.display_order)
                )
                for img in session.exec(imgs_stmt).all():
                    sid = str(img.selection_id)
                    images_by_selection.setdefault(sid, []).append(
                        {"id": str(img.id), "image_url": get_image_display_url(img.image_url), "display_order": img.display_order}
                    )

                sp_stmt = (
                    select(SelectionProduct)
                    .where(SelectionProduct.selection_id.in_(selection_ids))
                    .where(SelectionProduct.is_deleted == False)
                    .order_by(SelectionProduct.display_order)
                )
                sps = session.exec(sp_stmt).all()
                if sps:
                    product_ids = [sp.product_id for sp in sps]
                    prods_stmt = (
                        select(Product)
                        .where(Product.id.in_(product_ids))
                        .where(Product.is_deleted == False)
                    )
                    products_map = {p.id: p for p in session.exec(prods_stmt).all()}
                    for sp in sps:
                        sid = str(sp.selection_id)
                        prod = products_map.get(sp.product_id)
                        products_by_selection.setdefault(sid, []).append({
                            "id": str(sp.id),
                            "product_id": str(sp.product_id),
                            "display_order": sp.display_order,
                            "name": prod.name if prod else None,
                            "thumbnail_url": prod.thumbnail_url if prod else None,
                            "price": float(prod.price) if prod and prod.price else None,
                            "status": prod.status.value if prod else None,
                        })

            result = [
                {
                    "id": str(s.id),
                    "title": s.title,
                    "subtitle": s.subtitle,
                    "description": s.description,
                    "images": images_by_selection.get(str(s.id), []),
                    "products": products_by_selection.get(str(s.id), []),
                }
                for s in items
            ]

        total_pages = math.ceil(total / size) if size else 1
        return success_response(
            result,
            meta={"page": page, "size": size, "total_count": total, "total_pages": total_pages},
        )
    except AppError as e:
        return handle_app_error(e)


@selections_bp.route("/selections/{selection_id}", methods=["GET"], cors=True)
def get_selection(selection_id):
    try:
        with get_session() as session:
            selection = fetch(session, Selection, raise_not_found=True, id=selection_id)
            result = _serialize_selection(session, selection)
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@selections_bp.route("/selections/{selection_id}/products/{product_id}", methods=["GET"], cors=True)
def get_selection_product(selection_id, product_id):
    try:
        with get_session() as session:
            fetch(session, Selection, raise_not_found=True, id=selection_id)

            sp_stmt = (
                select(SelectionProduct)
                .where(SelectionProduct.selection_id == selection_id)
                .where(SelectionProduct.product_id == product_id)
                .where(SelectionProduct.is_deleted == False)
            )
            sp = session.exec(sp_stmt).first()
            if not sp:
                raise NotFoundError("해당 셀렉션 상품을 찾을 수 없습니다.")

            product = fetch(session, Product, raise_not_found=True, id=product_id)
            result = {
                "id": str(sp.id),
                "product_id": str(sp.product_id),
                "display_order": sp.display_order,
                "name": product.name,
                "thumbnail_url": product.thumbnail_url,
                "price": float(product.price) if product.price else None,
                "status": product.status.value,
            }
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@selections_bp.route("/selections", methods=["POST"], cors=True)
@require_admin
def create_selection():
    try:
        body = selections_bp.current_request.json_body or {}
        if not body.get("title"):
            raise ValidationError("title은 필수입니다.")

        with get_session() as session:
            selection = insert(session, Selection, {
                "title": body["title"],
                "subtitle": body.get("subtitle"),
                "description": body.get("description"),
            })
            result = _serialize_selection(session, selection)
        return success_response(result, status_code=201)
    except AppError as e:
        return handle_app_error(e)


@selections_bp.route("/selections/{selection_id}", methods=["PATCH"], cors=True)
@require_admin
def patch_selection(selection_id):
    try:
        body = selections_bp.current_request.json_body or {}
        allowed = {"title", "subtitle", "description"}
        data = {k: v for k, v in body.items() if k in allowed}

        with get_session() as session:
            selection = fetch(session, Selection, raise_not_found=True, id=selection_id)
            selection = update(session, selection, data)
            result = _serialize_selection(session, selection)
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@selections_bp.route("/selections/{selection_id}", methods=["DELETE"], cors=True)
@require_admin
def delete_selection(selection_id):
    try:
        with get_session() as session:
            selection = fetch(session, Selection, raise_not_found=True, id=selection_id)
            delete(session, selection)
        return success_response({"message": "삭제되었습니다."})
    except AppError as e:
        return handle_app_error(e)


@selections_bp.route("/selections/{selection_id}/products", methods=["POST"], cors=True)
@require_admin
def add_selection_product(selection_id):
    try:
        body = selections_bp.current_request.json_body or {}
        if not body.get("product_id"):
            raise ValidationError("product_id는 필수입니다.")

        with get_session() as session:
            fetch(session, Selection, raise_not_found=True, id=selection_id)
            fetch(session, Product, raise_not_found=True, id=body["product_id"])

            sp = insert(session, SelectionProduct, {
                "selection_id": selection_id,
                "product_id": body["product_id"],
                "display_order": body.get("display_order", 0),
            })
            result = {
                "id": str(sp.id),
                "selection_id": str(sp.selection_id),
                "product_id": str(sp.product_id),
                "display_order": sp.display_order,
            }
        return success_response(result, status_code=201)
    except AppError as e:
        return handle_app_error(e)


@selections_bp.route("/selections/{selection_id}/images/{image_id}", methods=["DELETE"], cors=True)
@require_admin
def delete_selection_image(selection_id, image_id):
    try:
        with get_session() as session:
            fetch(session, Selection, raise_not_found=True, id=selection_id)
            image = fetch(session, SelectionImage, raise_not_found=True, id=image_id)
            delete(session, image)
        return success_response({"message": "삭제되었습니다."})
    except AppError as e:
        return handle_app_error(e)


@selections_bp.route("/selections/{selection_id}/images", methods=["POST"], cors=True)
@require_admin
def add_selection_image(selection_id):
    try:
        body = selections_bp.current_request.json_body or {}
        if not body.get("image_url"):
            raise ValidationError("image_url은 필수입니다.")

        with get_session() as session:
            fetch(session, Selection, raise_not_found=True, id=selection_id)
            image = insert(session, SelectionImage, {
                "selection_id": selection_id,
                "image_url": body["image_url"],
                "display_order": body.get("display_order", 0),
            })
            result = {
                "id": str(image.id),
                "selection_id": str(image.selection_id),
                "image_url": get_image_display_url(image.image_url),
                "display_order": image.display_order,
            }
        return success_response(result, status_code=201)
    except AppError as e:
        return handle_app_error(e)
