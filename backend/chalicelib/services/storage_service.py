import uuid
import boto3
from botocore.config import Config
from urllib.parse import urlparse
from chalicelib.core.config import settings

_s3_client = None


def _get_s3_client():
    global _s3_client
    if _s3_client is None:
        # path-style addressing: required for bucket names containing dots (e.g. attiquedesign.com)
        # virtual-hosted style (bucket.s3.region.amazonaws.com) fails SSL validation for dotted names
        _s3_client = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
            config=Config(s3={"addressing_style": "path"}),
        )
    return _s3_client


def _path_style_prefix() -> str:
    return f"https://s3.{settings.AWS_REGION}.amazonaws.com/{settings.S3_BUCKET}/"


def _virtual_hosted_prefix() -> str:
    return f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/"


def _extract_object_key(stored_url: str) -> str | None:
    """Extract S3 object key from any stored URL format."""
    path_prefix = _path_style_prefix()
    virtual_prefix = _virtual_hosted_prefix()

    if stored_url.startswith(path_prefix):
        return stored_url[len(path_prefix):]
    if stored_url.startswith(virtual_prefix):
        return stored_url[len(virtual_prefix):]
    if stored_url.startswith("https://") or stored_url.startswith("http://"):
        # Unknown full URL — try extracting key from path, stripping leading /bucket/
        parsed = urlparse(stored_url)
        path = parsed.path.lstrip("/")
        bucket_prefix = settings.S3_BUCKET + "/"
        if path.startswith(bucket_prefix):
            return path[len(bucket_prefix):]
        return path
    # Already a bare object key
    return stored_url.lstrip("/")


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


def get_image_display_url(stored_url: str) -> str:
    """Return stable public URL for a stored S3 image.

    Uses path-style (https://s3.REGION.amazonaws.com/BUCKET/KEY) which has
    valid SSL certs even for bucket names containing dots.
    No presigning — images must be publicly readable via bucket policy.
    """
    if not stored_url:
        return stored_url

    key = _extract_object_key(stored_url)
    if not key:
        return stored_url

    return f"{_path_style_prefix()}{key}"


def get_public_url(object_key: str) -> str:
    return f"{_path_style_prefix()}{object_key}"
