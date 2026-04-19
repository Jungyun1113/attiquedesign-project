#!/usr/bin/env python3
"""
깨진 이미지 레코드 일괄 정리 스크립트.

S3에 실제 파일이 존재하지 않는 portfolio_images / selection_images 레코드를
소프트 딜리트(is_deleted = true)하고 재업로드가 필요한 목록을 출력합니다.

사용법:
    cd backend
    pip install python-dotenv boto3 sqlalchemy psycopg2-binary
    python scripts/cleanup_missing_images.py          # dry-run (기본값)
    python scripts/cleanup_missing_images.py --apply  # 실제 삭제 적용
"""
import argparse
import os
import sys

import boto3
from botocore.config import Config

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from sqlalchemy import create_engine, text

DB_URL = os.getenv("DATABASE_URL", "")
S3_BUCKET = os.getenv("S3_BUCKET", "attiquedesign.com")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
AWS_PROFILE = os.getenv("AWS_PROFILE", "attiquedesign")


def build_s3_key_set() -> set[str]:
    """S3 버킷에 실제 존재하는 portfolios/ + selections/ 키 목록을 반환합니다."""
    session = boto3.Session(profile_name=AWS_PROFILE)
    s3 = session.client("s3", region_name=AWS_REGION,
                        config=Config(s3={"addressing_style": "path"}))

    keys: set[str] = set()
    for prefix in ("portfolios/", "selections/"):
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []):
                keys.add(obj["Key"])
    return keys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="실제로 is_deleted=true 적용 (없으면 dry-run)")
    args = parser.parse_args()

    if not DB_URL:
        print("❌ DATABASE_URL 환경변수가 없습니다.")
        sys.exit(1)

    print("🔍 S3 파일 목록 조회 중...")
    existing_keys = build_s3_key_set()
    print(f"   S3 내 이미지: {len(existing_keys)}개\n")

    engine = create_engine(DB_URL)
    broken_portfolio: list[tuple] = []
    broken_selection: list[tuple] = []

    with engine.connect() as conn:
        for row in conn.execute(text("""
            SELECT pi.id, pi.image_url, p.category, p.title
            FROM portfolio_images pi
            JOIN portfolios p ON pi.portfolio_id = p.id
            WHERE pi.is_deleted = false
            ORDER BY p.category, p.title, pi.display_order
        """)).fetchall():
            if row[1] not in existing_keys:
                broken_portfolio.append(row)

        for row in conn.execute(text("""
            SELECT si.id, si.image_url, s.title
            FROM selection_images si
            JOIN selections s ON si.selection_id = s.id
            WHERE si.is_deleted = false
            ORDER BY s.title, si.display_order
        """)).fetchall():
            if row[1] not in existing_keys:
                broken_selection.append(row)

    print("=" * 60)
    print(f"재업로드 필요: 포트폴리오 이미지 {len(broken_portfolio)}개")
    print("=" * 60)
    for r in broken_portfolio:
        print(f"  [{r[2]}/{r[3]}]  {r[1]}")

    print()
    print("=" * 60)
    print(f"재업로드 필요: 셀렉션 이미지 {len(broken_selection)}개")
    print("=" * 60)
    for r in broken_selection:
        print(f"  [{r[2]}]  {r[1]}")

    total = len(broken_portfolio) + len(broken_selection)
    print(f"\n합계: {total}개 레코드가 S3에 파일 없음")

    if total == 0:
        print("✅ 모든 레코드가 정상입니다.")
        return

    if not args.apply:
        print("\n⚠️  dry-run 모드 — 실제 변경 없음. --apply 옵션으로 정리를 적용하세요.")
        return

    print("\n🗑️  is_deleted=true 처리 중...")
    with engine.connect() as conn:
        ids = [r[0] for r in broken_portfolio]
        if ids:
            conn.execute(
                text("UPDATE portfolio_images SET is_deleted=true WHERE id = ANY(:ids)"),
                {"ids": ids},
            )
        ids = [r[0] for r in broken_selection]
        if ids:
            conn.execute(
                text("UPDATE selection_images SET is_deleted=true WHERE id = ANY(:ids)"),
                {"ids": ids},
            )
        conn.commit()

    print(f"✅ {total}개 레코드 소프트 딜리트 완료.")
    print("   어드민 패널에서 이미지를 다시 업로드해 주세요.")


if __name__ == "__main__":
    main()
