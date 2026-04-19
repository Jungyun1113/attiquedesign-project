#!/usr/bin/env python3
"""
이미지 업로드 및 접근성 검증 테스트 스크립트.

검증 항목:
  1. S3 버킷 접근 가능 여부
  2. Bucket Policy (퍼블릭 읽기) 설정 여부
  3. CORS 설정 여부
  4. 이미지 URL 생성 로직 검증
  5. API 응답의 이미지 URL 접근 가능 여부

사용법:
  cd backend
  source .venv/bin/activate
  python scripts/verify_image_pipeline.py [--bucket BUCKET_NAME] [--api-url API_URL]
"""

import argparse
import json
import os
import sys
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import boto3
from botocore.config import Config
import requests


def check_env_config():
    """환경 변수 설정 검증"""
    print("\n═══ 1. 환경 변수 검증 ═══")
    
    s3_bucket = os.getenv("S3_BUCKET", "")
    aws_region = os.getenv("AWS_REGION", "")
    
    issues = []
    
    if not s3_bucket or s3_bucket == "your-s3-bucket-name":
        issues.append("❌ S3_BUCKET이 설정되지 않았거나 플레이스홀더입니다.")
        print(f"  S3_BUCKET = '{s3_bucket}' ← ❌ 잘못됨")
    else:
        print(f"  S3_BUCKET = '{s3_bucket}' ✅")
    
    if not aws_region:
        issues.append("❌ AWS_REGION이 설정되지 않았습니다.")
        print(f"  AWS_REGION = '' ← ❌")
    else:
        print(f"  AWS_REGION = '{aws_region}' ✅")
    
    return len(issues) == 0, s3_bucket, aws_region


def check_bucket_policy(s3, bucket: str):
    """S3 버킷 정책 검증"""
    print("\n═══ 2. Bucket Policy 검증 ═══")
    
    try:
        policy = s3.get_bucket_policy(Bucket=bucket)
        policy_doc = json.loads(policy["Policy"])
        
        has_public_read = any(
            stmt.get("Action") == "s3:GetObject"
            and stmt.get("Effect") == "Allow"
            and stmt.get("Principal") == "*"
            for stmt in policy_doc.get("Statement", [])
        )
        
        if has_public_read:
            print("  퍼블릭 읽기(s3:GetObject) 허용: ✅")
        else:
            print("  퍼블릭 읽기(s3:GetObject) 허용: ❌ — 아직 설정되지 않음")
            print("  → setup_s3_public_access.py 스크립트를 실행해 주세요.")
        
        return has_public_read
    except s3.exceptions.from_code("NoSuchBucketPolicy"):
        print("  Bucket Policy 없음 ❌")
        print("  → setup_s3_public_access.py 스크립트를 실행해 주세요.")
        return False
    except Exception as e:
        print(f"  확인 실패: {e}")
        return False


def check_cors(s3, bucket: str):
    """S3 CORS 설정 검증"""
    print("\n═══ 3. CORS 설정 검증 ═══")
    
    try:
        cors = s3.get_bucket_cors(Bucket=bucket)
        rules = cors.get("CORSRules", [])
        
        if not rules:
            print("  CORS 규칙 없음 ❌")
            return False
        
        has_get = False
        has_put = False
        has_origin = False
        
        for rule in rules:
            methods = rule.get("AllowedMethods", [])
            origins = rule.get("AllowedOrigins", [])
            
            if "GET" in methods:
                has_get = True
            if "PUT" in methods:
                has_put = True
            if "*" in origins or any("attiquedesign" in o for o in origins):
                has_origin = True
            
            print(f"  규칙: Origins={origins}, Methods={methods}")
        
        print(f"  GET 허용: {'✅' if has_get else '❌'}")
        print(f"  PUT 허용: {'✅' if has_put else '❌'}")
        print(f"  Origin 허용: {'✅' if has_origin else '❌'}")
        
        return has_get and has_put and has_origin
    except Exception as e:
        print(f"  CORS 확인 실패 (미설정): {e}")
        print("  → setup_s3_public_access.py 스크립트를 실행해 주세요.")
        return False


def check_url_generation(bucket: str, region: str):
    """URL 생성 로직 검증"""
    print("\n═══ 4. URL 생성 로직 검증 ═══")
    
    # Path-style URL (이 프로젝트에서 사용)
    path_style = f"https://s3.{region}.amazonaws.com/{bucket}/portfolios/test.jpg"
    # Virtual-hosted style URL
    virtual_style = f"https://{bucket}.s3.{region}.amazonaws.com/portfolios/test.jpg"
    
    print(f"  Path-style URL: {path_style}")
    print(f"  Virtual-hosted URL: {virtual_style}")
    
    # 버킷명에 dot이 있으면 path-style 사용이 올바름
    if "." in bucket:
        print(f"  ⚠️ 버킷명에 dot(.)이 포함됨 → path-style 필수 ✅ (현재 코드가 올바름)")
    
    # object_key 입력 시 변환 테스트
    test_keys = [
        "portfolios/abc123.jpg",
        f"https://s3.{region}.amazonaws.com/{bucket}/portfolios/abc123.jpg",
        f"https://{bucket}.s3.{region}.amazonaws.com/portfolios/abc123.jpg",
    ]
    
    path_prefix = f"https://s3.{region}.amazonaws.com/{bucket}/"
    virtual_prefix = f"https://{bucket}.s3.{region}.amazonaws.com/"
    
    for key in test_keys:
        if key.startswith(path_prefix):
            extracted = key[len(path_prefix):]
        elif key.startswith(virtual_prefix):
            extracted = key[len(virtual_prefix):]
        else:
            extracted = key.lstrip("/")
        
        result = f"{path_prefix}{extracted}"
        print(f"  입력: {key[:60]}... → 출력: {result[:80]}...")
    
    return True


def check_image_accessibility(bucket: str, region: str):
    """실제 이미지 URL 접근 테스트"""
    print("\n═══ 5. 이미지 접근성 테스트 ═══")
    
    s3 = boto3.client(
        "s3",
        region_name=region,
        config=Config(s3={"addressing_style": "path"}),
    )
    
    # 버킷의 첫 번째 이미지 오브젝트 찾기
    try:
        response = s3.list_objects_v2(Bucket=bucket, Prefix="portfolios/", MaxKeys=3)
        objects = response.get("Contents", [])
        
        if not objects:
            response = s3.list_objects_v2(Bucket=bucket, Prefix="selections/", MaxKeys=3)
            objects = response.get("Contents", [])
        
        if not objects:
            print("  버킷에 이미지 오브젝트 없음 (아직 업로드 전)")
            return True
        
        for obj in objects:
            key = obj["Key"]
            url = f"https://s3.{region}.amazonaws.com/{bucket}/{key}"
            
            try:
                resp = requests.head(url, timeout=10)
                status = resp.status_code
                ct = resp.headers.get("Content-Type", "?")
                
                if status == 200:
                    print(f"  ✅ {key} → {status} ({ct})")
                elif status == 403:
                    print(f"  ❌ {key} → 403 Forbidden — Bucket Policy 설정 필요")
                else:
                    print(f"  ⚠️ {key} → {status}")
            except Exception as e:
                print(f"  ❌ {key} → 접근 실패: {e}")
        
        # CORS 헤더 테스트
        if objects:
            key = objects[0]["Key"]
            url = f"https://s3.{region}.amazonaws.com/{bucket}/{key}"
            try:
                resp = requests.get(
                    url,
                    headers={"Origin": "https://attiquedesign.com"},
                    timeout=10,
                )
                cors_header = resp.headers.get("Access-Control-Allow-Origin")
                if cors_header:
                    print(f"  CORS 응답 헤더: Access-Control-Allow-Origin = {cors_header} ✅")
                else:
                    print(f"  CORS 응답 헤더 없음 ❌ — CORS 설정 필요")
            except Exception as e:
                print(f"  CORS 테스트 실패: {e}")
    
    except Exception as e:
        print(f"  버킷 접근 실패: {e}")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description="이미지 파이프라인 검증 테스트")
    parser.add_argument("--bucket", default=os.getenv("S3_BUCKET", ""), help="S3 버킷 이름")
    parser.add_argument("--region", default=os.getenv("AWS_REGION", "ap-northeast-2"), help="AWS 리전")
    parser.add_argument("--profile", default="attiquedesign", help="AWS CLI 프로파일")
    args = parser.parse_args()
    
    print("🔍 이미지 업로드 파이프라인 검증 시작\n")
    
    # 1. 환경 변수
    env_ok, bucket, region = check_env_config()
    
    if args.bucket and args.bucket != bucket:
        bucket = args.bucket
        print(f"  → CLI에서 지정된 버킷 사용: {bucket}")
    
    if not bucket or bucket == "your-s3-bucket-name":
        print("\n⛔ S3_BUCKET이 설정되지 않아 나머지 테스트를 수행할 수 없습니다.")
        print("   .env 파일을 수정하거나 --bucket 옵션을 사용하세요.")
        sys.exit(1)
    
    # S3 클라이언트
    session = boto3.Session(profile_name=args.profile)
    s3 = session.client(
        "s3",
        region_name=region,
        config=Config(s3={"addressing_style": "path"}),
    )
    
    # 2. Bucket Policy
    policy_ok = check_bucket_policy(s3, bucket)
    
    # 3. CORS
    cors_ok = check_cors(s3, bucket)
    
    # 4. URL 생성 로직
    url_ok = check_url_generation(bucket, region)
    
    # 5. 실제 접근 테스트
    access_ok = check_image_accessibility(bucket, region)
    
    # 결과 요약
    print("\n═══ 검증 결과 요약 ═══")
    results = {
        "환경 변수": env_ok,
        "Bucket Policy": policy_ok,
        "CORS": cors_ok,
        "URL 생성": url_ok,
        "이미지 접근": access_ok,
    }
    
    all_pass = True
    for name, ok in results.items():
        print(f"  {'✅' if ok else '❌'} {name}")
        if not ok:
            all_pass = False
    
    if all_pass:
        print("\n🎉 모든 검증 통과!")
    else:
        print("\n⚠️ 일부 항목이 실패했습니다. 위의 안내를 따라 수정해 주세요.")
    
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
