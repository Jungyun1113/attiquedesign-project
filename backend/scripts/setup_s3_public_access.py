#!/usr/bin/env python3
"""
S3 버킷 퍼블릭 읽기 정책 및 CORS 설정 스크립트.

이 스크립트는 다음 2가지를 수행합니다:
  1. Bucket Policy — s3:GetObject 퍼블릭 허용 (이미지 브라우저 접근)
  2. CORS 설정 — 사파리/크롬 모두에서 이미지 로드 허용

사용법:
  cd backend
  source .venv/bin/activate
  python scripts/setup_s3_public_access.py [--bucket BUCKET_NAME] [--dry-run]
"""

import argparse
import json
import sys
import os

import boto3
from botocore.config import Config

# .env 로드 (dotenv 있을 때)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_s3_client(region: str, profile: str | None = None):
    session_kwargs = {}
    if profile:
        session_kwargs["profile_name"] = profile
    session = boto3.Session(**session_kwargs)
    return session.client(
        "s3",
        region_name=region,
        config=Config(s3={"addressing_style": "path"}),
    )


def set_bucket_policy(s3, bucket: str, dry_run: bool):
    """S3 버킷에 퍼블릭 읽기 정책을 설정합니다."""
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket}/*",
            }
        ],
    }
    policy_json = json.dumps(policy, indent=2)

    print("\n📋 적용할 Bucket Policy:")
    print(policy_json)

    if dry_run:
        print("\n⏭️  [DRY-RUN] Bucket Policy 적용을 건너뜁니다.")
        return

    # 퍼블릭 액세스 차단 설정 해제 (필요 시)
    try:
        s3.put_public_access_block(
            Bucket=bucket,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False,
            },
        )
        print("✅ Public Access Block 해제 완료")
    except Exception as e:
        print(f"⚠️  Public Access Block 해제 실패 (사전에 해제됨일 수 있음): {e}")

    s3.put_bucket_policy(Bucket=bucket, Policy=policy_json)
    print("✅ Bucket Policy 적용 완료")


def set_cors(s3, bucket: str, allowed_origins: list[str], dry_run: bool):
    """S3 버킷에 CORS 규칙을 설정합니다."""
    cors_config = {
        "CORSRules": [
            {
                "AllowedOrigins": allowed_origins,
                "AllowedMethods": ["GET", "PUT", "POST", "HEAD"],
                "AllowedHeaders": ["*"],
                "ExposeHeaders": ["ETag"],
                "MaxAgeSeconds": 86400,
            }
        ]
    }

    print("\n📋 적용할 CORS 설정:")
    print(json.dumps(cors_config, indent=2))

    if dry_run:
        print("\n⏭️  [DRY-RUN] CORS 적용을 건너뜁니다.")
        return

    s3.put_bucket_cors(Bucket=bucket, CORSConfiguration=cors_config)
    print("✅ CORS 설정 적용 완료")


def verify_setup(s3, bucket: str):
    """설정이 올바르게 적용되었는지 검증합니다."""
    print("\n🔍 설정 검증 중...")

    # Bucket Policy 확인
    try:
        policy = s3.get_bucket_policy(Bucket=bucket)
        policy_doc = json.loads(policy["Policy"])
        has_public_read = any(
            stmt.get("Action") == "s3:GetObject"
            and stmt.get("Effect") == "Allow"
            and stmt.get("Principal") == "*"
            for stmt in policy_doc.get("Statement", [])
        )
        print(f"  Bucket Policy 퍼블릭 읽기: {'✅' if has_public_read else '❌'}")
    except Exception as e:
        print(f"  Bucket Policy 확인 실패: {e}")

    # CORS 확인
    try:
        cors = s3.get_bucket_cors(Bucket=bucket)
        rules = cors.get("CORSRules", [])
        print(f"  CORS 규칙 수: {len(rules)}")
        for i, rule in enumerate(rules):
            print(f"    규칙 {i + 1}: Origins={rule.get('AllowedOrigins')}, Methods={rule.get('AllowedMethods')}")
        print("  CORS 설정: ✅")
    except Exception as e:
        print(f"  CORS 확인 실패: {e}")


def main():
    parser = argparse.ArgumentParser(description="S3 버킷 퍼블릭 읽기 및 CORS 설정")
    parser.add_argument("--bucket", default=os.getenv("S3_BUCKET", ""), help="S3 버킷 이름")
    parser.add_argument("--region", default=os.getenv("AWS_REGION", "ap-northeast-2"), help="AWS 리전")
    parser.add_argument("--profile", default=os.getenv("AWS_PROFILE", "attiquedesign"), help="AWS CLI 프로파일")
    parser.add_argument("--origins", default="*", help="CORS 허용 Origins (쉼표 구분)")
    parser.add_argument("--dry-run", action="store_true", help="실제 적용 없이 계획만 출력")
    args = parser.parse_args()

    bucket = args.bucket
    if not bucket or bucket == "your-s3-bucket-name":
        print("❌ S3_BUCKET이 설정되지 않았습니다.")
        print("   .env 파일에서 S3_BUCKET을 실제 버킷명으로 설정하거나")
        print("   --bucket 옵션으로 전달해 주세요.")
        print("   예: python scripts/setup_s3_public_access.py --bucket attiquedesign.com")
        sys.exit(1)

    origins = [o.strip() for o in args.origins.split(",") if o.strip()]

    print(f"🪣 대상 버킷: {bucket}")
    print(f"🌍 리전: {args.region}")
    print(f"👤 프로파일: {args.profile}")
    print(f"🔗 CORS Origins: {origins}")

    s3 = get_s3_client(args.region, args.profile)

    # 1. Bucket Policy 설정
    set_bucket_policy(s3, bucket, args.dry_run)

    # 2. CORS 설정
    set_cors(s3, bucket, origins, args.dry_run)

    # 3. 검증
    if not args.dry_run:
        verify_setup(s3, bucket)

    print("\n🎉 완료!")


if __name__ == "__main__":
    main()
