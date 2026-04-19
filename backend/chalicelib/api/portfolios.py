import math
from chalice import Blueprint
from sqlmodel import select

from chalicelib.core.db import get_session
from chalicelib.core.auth import require_admin
from chalicelib.core.exceptions import success_response, handle_app_error, AppError, ValidationError
from chalicelib.helpers.db import fetch, bulk_fetch, insert, update, delete
from chalicelib.models.portfolio import Portfolio, PortfolioImage
from chalicelib.services.storage_service import get_image_display_url

portfolios_bp = Blueprint(__name__)


def _img_dict(img: PortfolioImage) -> dict:
    return {
        "id": str(img.id),
        "image_url": get_image_display_url(img.image_url),
        "display_order": img.display_order,
    }


def _serialize_portfolio(session, p: Portfolio) -> dict:
    images_stmt = (
        select(PortfolioImage)
        .where(PortfolioImage.portfolio_id == p.id)
        .where(PortfolioImage.is_deleted == False)
        .order_by(PortfolioImage.display_order)
    )
    images = session.exec(images_stmt).all()
    return {
        "id": str(p.id),
        "category": p.category,
        "title": p.title,
        "description": p.description,
        "cover_image_url": get_image_display_url(p.cover_image_url) if p.cover_image_url else None,
        "images": [_img_dict(img) for img in images],
    }


@portfolios_bp.route("/portfolios", methods=["GET"], cors=True)
def list_portfolios():
    try:
        params = portfolios_bp.current_request.query_params or {}
        page = int(params.get("page", 1))
        size = min(int(params.get("limit", 20)), 100)
        category = params.get("category")

        filters = {}
        if category:
            filters["category"] = category

        with get_session() as session:
            # Modify bulk_fetch behavior or just order manually here
            stmt = select(Portfolio)
            if category:
                stmt = stmt.where(Portfolio.category == category)
            stmt = stmt.order_by(Portfolio.sort_order)
            
            # Since bulk_fetch is a helper, let's see if we can use it with order_by
            # or just re-implement pagination here if needed.
            # Looking at portfolios.py:54, it uses bulk_fetch.
            # Let's try to pass order_by if supported, else manual query.
            items, total = bulk_fetch(session, Portfolio, filters=filters, page=page, size=size, order_by=Portfolio.sort_order)

            # Batch fetch all images in one query instead of N+1
            portfolio_ids = [p.id for p in items]
            images_by_portfolio: dict = {}
            if portfolio_ids:
                imgs_stmt = (
                    select(PortfolioImage)
                    .where(PortfolioImage.portfolio_id.in_(portfolio_ids))
                    .where(PortfolioImage.is_deleted == False)
                    .order_by(PortfolioImage.display_order)
                )
                for img in session.exec(imgs_stmt).all():
                    pid = str(img.portfolio_id)
                    images_by_portfolio.setdefault(pid, []).append(img)

            result = [
                {
                    "id": str(p.id),
                    "category": p.category,
                    "title": p.title,
                    "description": p.description,
                    "cover_image_url": get_image_display_url(p.cover_image_url) if p.cover_image_url else None,
                    "images": [_img_dict(img) for img in images_by_portfolio.get(str(p.id), [])],
                }
                for p in items
            ]

        total_pages = math.ceil(total / size) if size else 1
        return success_response(
            result,
            meta={"page": page, "size": size, "total_count": total, "total_pages": total_pages},
        )
    except AppError as e:
        return handle_app_error(e)


@portfolios_bp.route("/portfolios/{portfolio_id}", methods=["GET"], cors=True)
def get_portfolio(portfolio_id):
    try:
        with get_session() as session:
            portfolio = fetch(session, Portfolio, raise_not_found=True, id=portfolio_id)
            result = _serialize_portfolio(session, portfolio)
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@portfolios_bp.route("/portfolios", methods=["POST"], cors=True)
@require_admin
def create_portfolio():
    try:
        body = portfolios_bp.current_request.json_body or {}
        required = ["category", "title"]
        missing = [f for f in required if not body.get(f)]
        if missing:
            raise ValidationError(f"필수 필드 누락: {', '.join(missing)}")

        with get_session() as session:
            portfolio = insert(session, Portfolio, {
                "category": body["category"],
                "title": body["title"],
                "description": body.get("description"),
                "cover_image_url": body.get("cover_image_url"),
            })
            result = _serialize_portfolio(session, portfolio)
        return success_response(result, status_code=201)
    except AppError as e:
        return handle_app_error(e)


@portfolios_bp.route("/portfolios/{portfolio_id}", methods=["PATCH"], cors=True)
@require_admin
def patch_portfolio(portfolio_id):
    try:
        body = portfolios_bp.current_request.json_body or {}
        allowed = {"category", "title", "description", "cover_image_url"}
        data = {k: v for k, v in body.items() if k in allowed}

        with get_session() as session:
            portfolio = fetch(session, Portfolio, raise_not_found=True, id=portfolio_id)
            portfolio = update(session, portfolio, data)
            result = _serialize_portfolio(session, portfolio)
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@portfolios_bp.route("/admin/portfolios/reorder", methods=["POST"], cors=True)
@require_admin
def reorder_portfolios():
    try:
        body = portfolios_bp.current_request.json_body or {}
        orders = body.get("orders", [])  # [{id, sort_order}, ...]
        if not orders:
            raise ValidationError("orders는 필수입니다.")

        with get_session() as session:
            for item in orders:
                p = fetch(session, Portfolio, raise_not_found=True, id=item["id"])
                update(session, p, {"sort_order": item["sort_order"]})
        return success_response({"message": "포트폴리오 순서가 저장되었습니다."})
    except AppError as e:
        return handle_app_error(e)


@portfolios_bp.route("/portfolios/{portfolio_id}", methods=["DELETE"], cors=True)
@require_admin
def delete_portfolio(portfolio_id):
    try:
        with get_session() as session:
            portfolio = fetch(session, Portfolio, raise_not_found=True, id=portfolio_id)
            delete(session, portfolio)
        return success_response({"message": "삭제되었습니다."})
    except AppError as e:
        return handle_app_error(e)


# POST to avoid CORS preflight issues with PATCH in Chalice 1.x
@portfolios_bp.route("/portfolios/{portfolio_id}/reorder", methods=["POST"], cors=True)
@require_admin
def reorder_portfolio_images(portfolio_id):
    try:
        body = portfolios_bp.current_request.json_body or {}
        orders = body.get("orders", [])  # [{id, display_order}, ...]
        if not orders:
            raise ValidationError("orders는 필수입니다.")

        with get_session() as session:
            fetch(session, Portfolio, raise_not_found=True, id=portfolio_id)
            for item in orders:
                image = fetch(session, PortfolioImage, raise_not_found=True, id=item["id"])
                update(session, image, {"display_order": item["display_order"]})
        return success_response({"message": "순서가 저장되었습니다."})
    except AppError as e:
        return handle_app_error(e)


@portfolios_bp.route("/portfolios/{portfolio_id}/images/{image_id}", methods=["DELETE"], cors=True)
@require_admin
def delete_portfolio_image(portfolio_id, image_id):
    try:
        with get_session() as session:
            fetch(session, Portfolio, raise_not_found=True, id=portfolio_id)
            image = fetch(session, PortfolioImage, raise_not_found=True, id=image_id)
            delete(session, image)
        return success_response({"message": "삭제되었습니다."})
    except AppError as e:
        return handle_app_error(e)


@portfolios_bp.route("/portfolios/{portfolio_id}/images", methods=["POST"], cors=True)
@require_admin
def add_portfolio_image(portfolio_id):
    try:
        body = portfolios_bp.current_request.json_body or {}
        if not body.get("image_url"):
            raise ValidationError("image_url은 필수입니다.")

        with get_session() as session:
            fetch(session, Portfolio, raise_not_found=True, id=portfolio_id)
            image = insert(session, PortfolioImage, {
                "portfolio_id": portfolio_id,
                "image_url": body["image_url"],
                "display_order": body.get("display_order", 0),
            })
            print(f"DEBUG: Saved Portfolio Image - ID: {image.id}, URL stored: {image.image_url}")
            result = {
                "id": str(image.id),
                "portfolio_id": str(image.portfolio_id),
                "image_url": get_image_display_url(image.image_url),
                "display_order": image.display_order,
            }
        return success_response(result, status_code=201)
    except AppError as e:
        return handle_app_error(e)
