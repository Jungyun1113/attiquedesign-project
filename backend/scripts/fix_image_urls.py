#!/usr/bin/env python3
"""
기존 DB에 저장된 이미지 URL을 올바른 object_key 형식으로 정규화하는 마이그레이션 스크립트.

문제:
  기존에 presigned URL에서 쿼리 파라미터만 떼어낸 전체 URL이 DB에 저장됨.
  예: https://s3.ap-northeast-2.amazonaws.com/your-s3-bucket-name/portfolios/abc.jpg
  또는: https://s3.ap-northeast-2.amazonaws.com/attiquedesign.com/portfolios/abc.jpg

해결:
  모든 이미지 URL에서 object key만 추출하여 bare key 형태로 정규화.
  예: portfolios/abc.jpg

  이렇게 하면 백엔드의 get_image_display_url()이 올바른 S3_BUCKET 설정을 사용하여
  public URL을 동적으로 조합합니다.

사용법:
  cd backend
  source .venv/bin/activate
  python scripts/fix_image_urls.py --dry-run   # 먼저 확인
  python scripts/fix_image_urls.py              # 실제 적용
"""

import argparse
import os
import sys
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from sqlmodel import select, Session
from sqlalchemy import create_engine, text


DB_URL = os.getenv("DATABASE_URL", "")
S3_BUCKET = os.getenv("S3_BUCKET", "attiquedesign.com")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")

# 잘못된 버킷명들 (플레이스홀더 포함)
KNOWN_WRONG_BUCKETS = {"your-s3-bucket-name"}

# URL 프리픽스 패턴들
def _known_prefixes():
    prefixes = []
    all_buckets = {S3_BUCKET} | KNOWN_WRONG_BUCKETS
    for bucket in all_buckets:
        prefixes.append(f"https://s3.{AWS_REGION}.amazonaws.com/{bucket}/")
        prefixes.append(f"https://{bucket}.s3.{AWS_REGION}.amazonaws.com/")
        prefixes.append(f"https://s3.amazonaws.com/{bucket}/")
    return prefixes


def extract_object_key(url: str) -> str:
    """URL에서 S3 object key만 추출"""
    if not url:
        return url
    
    for prefix in _known_prefixes():
        if url.startswith(prefix):
            return url[len(prefix):]
    
    # 다른 형태의 S3 URL 시도
    if url.startswith("https://") or url.startswith("http://"):
        parsed = urlparse(url)
        path = parsed.path.lstrip("/")
        # path가 bucket/key 형태인지 확인
        all_buckets = {S3_BUCKET} | KNOWN_WRONG_BUCKETS
        for bucket in all_buckets:
            bucket_prefix = bucket + "/"
            if path.startswith(bucket_prefix):
                return path[len(bucket_prefix):]
        # 이미 key만 있거나 알 수 없는 URL
        return path if path else url
    
    # 이미 bare key
    return url.lstrip("/")


def fix_table(engine, table_name: str, url_column: str, dry_run: bool) -> int:
    """테이블의 이미지 URL을 정규화"""
    fixed = 0
    
    with engine.connect() as conn:
        rows = conn.execute(
            text(f"SELECT id, {url_column} FROM {table_name} WHERE {url_column} IS NOT NULL AND is_deleted = false")
        ).fetchall()
        
        for row in rows:
            row_id, current_url = row[0], row[1]
            if not current_url:
                continue
            
            new_key = extract_object_key(current_url)
            
            if new_key != current_url:
                print(f"  [{table_name}] {row_id}")
                print(f"    변경 전: {current_url[:100]}...")
                print(f"    변경 후: {new_key}")
                
                if not dry_run:
                    conn.execute(
                        text(f"UPDATE {table_name} SET {url_column} = :new_key WHERE id = :id"),
                        {"new_key": new_key, "id": row_id}
                    )
                fixed += 1
        
        if not dry_run and fixed > 0:
            conn.commit()
    
    return fixed


def main():
    parser = argparse.ArgumentParser(description="DB 이미지 URL 정규화")
    parser.add_argument("--dry-run", action="store_true", help="실제 변경 없이 확인만")
    args = parser.parse_args()

    if not DB_URL:
        print("❌ DATABASE_URL이 설정되지 않았습니다.")
        sys.exit(1)

    engine = create_engine(DB_URL)

    mode = "DRY-RUN (확인만)" if args.dry_run else "실제 적용"
    print(f"🔧 이미지 URL 정규화 시작 ({mode})\n")
    print(f"  S3_BUCKET: {S3_BUCKET}")
    print(f"  AWS_REGION: {AWS_REGION}")
    print()

    # 이미지 URL이 저장된 테이블들
    tables = [
        ("portfolio_images", "image_url"),
        ("portfolios", "cover_image_url"),
        ("selection_images", "image_url"),
    ]

    total_fixed = 0
    for table_name, url_column in tables:
        print(f"\n── {table_name}.{url_column} ──")
        try:
            count = fix_table(engine, table_name, url_column, args.dry_run)
            total_fixed += count
            if count == 0:
                print("  변경 사항 없음 ✅")
        except Exception as e:
            print(f"  오류: {e}")

    print(f"\n{'─' * 40}")
    if total_fixed > 0:
        if args.dry_run:
            print(f"📋 {total_fixed}개 URL이 변경 대상입니다.")
            print("   --dry-run 없이 다시 실행하면 실제 적용됩니다.")
        else:
            print(f"✅ {total_fixed}개 URL이 정규화되었습니다.")
    else:
        print("✅ 모든 URL이 이미 올바른 형식입니다.")


if __name__ == "__main__":
    main()
