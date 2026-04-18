import uuid
import boto3
from chalicelib.core.config import settings


def generate_presigned_put_url(filename: str, content_type: str, target: str) -> dict:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
    object_key = f"{target}/{uuid.uuid4()}.{ext}"

    s3_client = boto3.client("s3", region_name=settings.AWS_REGION)
    upload_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": object_key,
            "ContentType": content_type,
        },
        ExpiresIn=settings.PRESIGN_EXPIRY_SECONDS,
    )
    return {"upload_url": upload_url, "object_key": object_key}


def get_public_url(object_key: str) -> str:
    return f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{object_key}"
