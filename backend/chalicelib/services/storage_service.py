import io
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
            config=Config(
                s3={"addressing_style": "path"},
                signature_version="s3v4"
            ),
        )
    return _s3_client


def _path_style_prefix() -> str:
    return f"https://s3.{settings.AWS_REGION}.amazonaws.com/{settings.S3_BUCKET}/"


def _virtual_hosted_prefix() -> str:
    return f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/"


def _extract_object_key(stored_url: str) -> str | None:
    """Extract S3 object key from any stored URL format."""
    if not stored_url or stored_url.startswith("blob:"):
        return None

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
        # If it's a full URL but not from our bucket, we can't get a key
        return None
    # Already a bare object key
    return stored_url.lstrip("/")


def generate_presigned_put_url(filename: str, content_type: str, target: str) -> dict:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
    object_key = f"{target}/{uuid.uuid4()}.{ext}"

    # ContentType을 Params에 포함하여 서명함으로써 브라우저의 자동 헤더 추가와 일치시킵니다.
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


def optimize_image_in_s3(source_key: str) -> dict:
    """Download raw image from S3, convert to WebP (max 2400px, q=82), re-upload.

    Returns {optimized_key, original_bytes, optimized_bytes}.
    Falls back to the original key if Pillow is unavailable or processing fails.
    """
    try:
        from PIL import Image
    except ImportError:
        return {"optimized_key": source_key, "original_bytes": 0, "optimized_bytes": 0}

    s3 = _get_s3_client()

    # Download original
    obj = s3.get_object(Bucket=settings.S3_BUCKET, Key=source_key)
    original_bytes_data = obj["Body"].read()
    original_size = len(original_bytes_data)

    try:
        img = Image.open(io.BytesIO(original_bytes_data))

        # Preserve EXIF orientation before any transform
        try:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

        # Convert RGBA/P → RGB for WebP compatibility
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        # Downscale if either dimension exceeds 2400px
        max_dim = 2400
        if img.width > max_dim or img.height > max_dim:
            img.thumbnail((max_dim, max_dim), Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=82, method=4)
        optimized_data = buf.getvalue()
        optimized_size = len(optimized_data)

        # Build new key with .webp extension
        base = source_key.rsplit(".", 1)[0] if "." in source_key else source_key
        optimized_key = f"{base}.webp"

        s3.put_object(
            Bucket=settings.S3_BUCKET,
            Key=optimized_key,
            Body=optimized_data,
            ContentType="image/webp",
        )

        # Delete the original only if it differs from the optimized key
        if optimized_key != source_key:
            try:
                s3.delete_object(Bucket=settings.S3_BUCKET, Key=source_key)
            except Exception:
                pass

        return {
            "optimized_key": optimized_key,
            "original_bytes": original_size,
            "optimized_bytes": optimized_size,
        }

    except Exception:
        # If anything goes wrong, return the original untouched
        return {
            "optimized_key": source_key,
            "original_bytes": original_size,
            "optimized_bytes": original_size,
        }
