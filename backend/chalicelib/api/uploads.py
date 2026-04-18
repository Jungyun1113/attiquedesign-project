from chalice import Blueprint

from chalicelib.core.auth import require_admin
from chalicelib.core.exceptions import success_response, handle_app_error, AppError, ValidationError
from chalicelib.services.storage_service import generate_presigned_put_url

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
