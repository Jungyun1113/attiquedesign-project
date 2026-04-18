from chalice import Response
import json


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, message: str = "리소스를 찾을 수 없습니다."):
        super().__init__("NOT_FOUND", message, 404)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "인증이 필요합니다."):
        super().__init__("UNAUTHORIZED", message, 401)


class ForbiddenError(AppError):
    def __init__(self, message: str = "접근 권한이 없습니다."):
        super().__init__("FORBIDDEN", message, 403)


class ValidationError(AppError):
    def __init__(self, message: str = "입력값이 올바르지 않습니다."):
        super().__init__("VALIDATION_FAILED", message, 422)


class ConflictError(AppError):
    def __init__(self, message: str = "이미 존재하는 데이터입니다."):
        super().__init__("CONFLICT", message, 409)


def error_response(code: str, message: str, status_code: int = 400) -> Response:
    body = json.dumps({"success": False, "error": {"code": code, "message": message}})
    return Response(
        body=body,
        status_code=status_code,
        headers={"Content-Type": "application/json"},
    )


def success_response(data=None, meta: dict = None, status_code: int = 200) -> Response:
    payload: dict = {"success": True, "data": data}
    if meta is not None:
        payload["meta"] = meta
    return Response(
        body=json.dumps(payload, default=str),
        status_code=status_code,
        headers={"Content-Type": "application/json"},
    )


def handle_app_error(exc: AppError) -> Response:
    return error_response(exc.code, exc.message, exc.status_code)
