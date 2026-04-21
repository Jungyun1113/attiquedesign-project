from chalice import Blueprint

from chalicelib.core.db import get_session
from chalicelib.core.auth import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)
from chalicelib.core.exceptions import (
    AppError, UnauthorizedError, ConflictError, ValidationError,
    success_response, handle_app_error,
)
from chalicelib.helpers.db import fetch, insert
from chalicelib.models.user import User, UserRole, AuthProvider

auth_bp = Blueprint(__name__)


@auth_bp.route("/auth/register", methods=["POST"], cors=True)
def register():
    try:
        body = auth_bp.current_request.json_body or {}
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")
        name = body.get("name", "").strip()
        phone = body.get("phone")

        if not email or not password or not name:
            raise ValidationError("email, password, name은 필수입니다.")
        if len(password) < 8:
            raise ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")

        with get_session() as session:
            existing = fetch(session, User, email=email)
            if existing:
                raise ConflictError("이미 사용 중인 이메일입니다.")

            user = insert(session, User, {
                "email": email,
                "password_hash": hash_password(password),
                "name": name,
                "phone": phone,
                "role": UserRole.USER,
                "auth_provider": AuthProvider.LOCAL,
            })

            access_token = create_access_token(str(user.id), user.role.value)
            refresh_token = create_refresh_token(str(user.id))

        return success_response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
            },
            status_code=201,
        )
    except AppError as e:
        return handle_app_error(e)


@auth_bp.route("/auth/login", methods=["POST"], cors=True)
def login():
    try:
        body = auth_bp.current_request.json_body or {}
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")

        if not email or not password:
            raise ValidationError("email과 password는 필수입니다.")

        with get_session() as session:
            user = fetch(session, User, email=email)
            if not user or not user.password_hash:
                raise UnauthorizedError("이메일 또는 비밀번호가 올바르지 않습니다.")
            if not verify_password(password, user.password_hash):
                raise UnauthorizedError("이메일 또는 비밀번호가 올바르지 않습니다.")

            access_token = create_access_token(str(user.id), user.role.value)
            refresh_token = create_refresh_token(str(user.id))

        return success_response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        })
    except AppError as e:
        return handle_app_error(e)
    except Exception as e:
        print(f"ERROR: Login failure: {e}")
        return handle_app_error(AppError("서버 오류가 발생했습니다. DB 상태를 확인해주세요.", status_code=500))


@auth_bp.route("/auth/refresh", methods=["POST"], cors=True)
def refresh():
    """Refresh Token으로 새 Access Token 발급."""
    try:
        body = auth_bp.current_request.json_body or {}
        refresh_token = body.get("refresh_token", "")
        if not refresh_token:
            raise ValidationError("refresh_token은 필수입니다.")

        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise UnauthorizedError("유효하지 않은 refresh token입니다.")

        user_id = payload.get("sub")

        with get_session() as session:
            user = fetch(session, User, raise_not_found=True, id=user_id)
            new_access_token = create_access_token(str(user.id), user.role.value)
            new_refresh_token = create_refresh_token(str(user.id))

        return success_response({
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "Bearer",
        })
    except AppError as e:
        return handle_app_error(e)


@auth_bp.route("/auth/password", methods=["PATCH"], cors=True)
def change_password():
    """현재 비밀번호 확인 후 새 비밀번호로 변경."""
    try:
        request = auth_bp.current_request
        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            raise UnauthorizedError()

        token = auth_header[len("Bearer "):]
        payload = decode_token(token)

        body = request.json_body or {}
        current_password = body.get("current_password", "")
        new_password = body.get("new_password", "")

        if not current_password or not new_password:
            raise ValidationError("current_password와 new_password는 필수입니다.")
        if len(new_password) < 8:
            raise ValidationError("새 비밀번호는 최소 8자 이상이어야 합니다.")

        with get_session() as session:
            user = fetch(session, User, raise_not_found=True, id=payload["sub"])
            if not verify_password(current_password, user.password_hash):
                raise UnauthorizedError("현재 비밀번호가 올바르지 않습니다.")
            user.password_hash = hash_password(new_password)
            session.add(user)

        return success_response({"message": "비밀번호가 변경되었습니다."})
    except AppError as e:
        return handle_app_error(e)


@auth_bp.route("/auth/me", methods=["GET"], cors=True)
def me():
    """현재 로그인된 사용자 정보 조회."""
    try:
        request = auth_bp.current_request
        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            raise UnauthorizedError()

        token = auth_header[len("Bearer "):]
        payload = decode_token(token)

        with get_session() as session:
            user = fetch(session, User, raise_not_found=True, id=payload["sub"])
            result = {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
                "role": user.role.value,
                "auth_provider": user.auth_provider.value,
            }

        return success_response(result)
    except AppError as e:
        return handle_app_error(e)
