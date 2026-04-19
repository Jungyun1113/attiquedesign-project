from chalice import Blueprint

from chalicelib.core.auth import require_admin
from chalicelib.core.exceptions import success_response, handle_app_error, AppError, ValidationError
from chalicelib.services.storage_service import generate_presigned_put_url, optimize_image_in_s3

uploads_bp = Blueprint(__name__)

ALLOWED_TARGETS = {"products", "portfolios", "selections", "avatars"}


@uploads_bp.route("/uploads/presign", methods=["POST"], cors=True)
@require_admin
def presign():
    try:
        body = uploads_bp.current_request.json_body or {}
        filename = body.get("filename", "").strip()
        content_type = body.get("content_type", "").strip()
        target = body.get("target", "").strip()

        if not filename or not content_type or not target:
            raise ValidationError("filename, content_type, target은 필수입니다.")

        if target not in ALLOWED_TARGETS:
            raise ValidationError(f"허용된 target: {', '.join(ALLOWED_TARGETS)}")

        result = generate_presigned_put_url(filename, content_type, target)
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)


@uploads_bp.route("/uploads/optimize", methods=["POST"], cors=True)
@require_admin
def optimize():
    """Download a freshly-uploaded S3 object, convert to WebP, re-upload.

    Request body: { "object_key": "portfolios/uuid.jpg" }
    Response:     { "optimized_key": "portfolios/uuid.webp",
                    "original_bytes": 2048000,
                    "optimized_bytes": 184320 }
    """
    try:
        body = uploads_bp.current_request.json_body or {}
        object_key = body.get("object_key", "").strip()

        if not object_key:
            raise ValidationError("object_key는 필수입니다.")

        # Basic path traversal guard
        if ".." in object_key or object_key.startswith("/"):
            raise ValidationError("유효하지 않은 object_key입니다.")

        result = optimize_image_in_s3(object_key)
        return success_response(result)
    except AppError as e:
        return handle_app_error(e)
