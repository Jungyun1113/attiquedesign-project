import uuid
import boto3
from urllib.parse import urlparse
from chalicelib.core.config import settings

_s3_client = None
_S3_PREFIX = None


def _get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3", region_name=settings.AWS_REGION)
    return _s3_client


def _s3_prefix() -> str:
    global _S3_PREFIX
    if _S3_PREFIX is None:
        _S3_PREFIX = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/"
    return _S3_PREFIX


def generate_presigned_put_url(filename: str, content_type: str, target: str) -> dict:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
    object_key = f"{target}/{uuid.uuid4()}.{ext}"

    upload_url = _get_s3_client().generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": object_key,
            "ContentType": content_type,
        },
        ExpiresIn=settings.PRESIGN_EXPIRY_SECONDS,
    )
    return {"upload_url": upload_url, "object_key": object_key}


def get_image_display_url(stored_url: str, expires_in: int = 3600) -> str:
    """Convert a stored S3 URL to a presigned GET URL for display.
    Pure local crypto — no HTTP call to S3, very fast.
    """
    if not stored_url:
        return stored_url
    prefix = _s3_prefix()
    if stored_url.startswith(prefix):
        object_key = stored_url[len(prefix):]
    else:
        object_key = urlparse(stored_url).path.lstrip("/")

    return _get_s3_client().generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": object_key},
        ExpiresIn=expires_in,
    )


def get_public_url(object_key: str) -> str:
    return f"{_s3_prefix()}{object_key}"
