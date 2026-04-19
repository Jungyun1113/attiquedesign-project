#!/usr/bin/env python3
import os
import sys
from urllib.parse import urlparse
from sqlalchemy import create_engine, text

# .env 로드
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_URL = os.getenv("DATABASE_URL", "")
S3_BUCKET = os.getenv("S3_BUCKET", "attiquedesign.com")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")

def get_prefixes():
    return [
        f"https://s3.{AWS_REGION}.amazonaws.com/{S3_BUCKET}/",
        f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/",
        f"https://s3.amazonaws.com/{S3_BUCKET}/",
        "https://s3.ap-northeast-2.amazonaws.com/your-s3-bucket-name/",
    ]

def normalize_key(url: str) -> str | None:
    if not url: return None
    if url.startswith("blob:"): return "DELETE"
    
    # 1. Known S3 Prefixes 제거
    for p in get_prefixes():
        if url.startswith(p):
            return url[len(p):]
    
    # 2. http(s) URL인데 우리 버킷 것이 아닌 경우 (또는 분석 불가)
    if url.startswith("http"):
        parsed = urlparse(url)
        path = parsed.path.lstrip("/")
        if S3_BUCKET in path:
            return path.split(S3_BUCKET + "/")[-1]
        # 알려지지 않은 타 도메인 URL이면 일단 유지하거나 DELETE 결정 (여기선 비정상으로 간주)
        if "s3.amazonaws.com" not in url:
            return "DELETE"
        return path

    # 3. 이미 Key 형태 (예: portfolios/...)
    if url.startswith("portfolios/") or url.startswith("selections/") or url.startswith("products/"):
        return url.lstrip("/")
        
    # 4. 그 외 알 수 없는 문자열
    return "DELETE"

def clean():
    if not DB_URL:
        print("❌ DATABASE_URL missing")
        return

    engine = create_engine(DB_URL)
    tables = [
        ("portfolio_images", "image_url"),
        ("portfolios", "cover_image_url"),
        ("selection_images", "image_url"),
        ("products", "main_image_url"),
    ]

    total_fixed = 0
    total_deleted = 0

    with engine.connect() as conn:
        for table, col in tables:
            print(f"\n🔍 Processing {table}.{col}...")
            # is_deleted 필드가 있는 경우 반영
            try:
                rows = conn.execute(text(f"SELECT id, {col} FROM {table} WHERE {col} IS NOT NULL")).fetchall()
            except Exception as e:
                print(f"Skipping {table}: {e}")
                continue

            for row_id, val in rows:
                action = normalize_key(val)
                
                if action == "DELETE":
                    print(f"  [DEL] {row_id}: {val[:50]}...")
                    conn.execute(text(f"DELETE FROM {table} WHERE id = :id"), {"id": row_id})
                    total_deleted += 1
                elif action and action != val:
                    print(f"  [FIX] {row_id}: {val[:30]} -> {action}")
                    conn.execute(text(f"UPDATE {table} SET {col} = :val WHERE id = :id"), {"val": action, "id": row_id})
                    total_fixed += 1
        
        conn.commit()

    print(f"\n✨ Done! Fixed: {total_fixed}, Deleted: {total_deleted}")

if __name__ == "__main__":
    clean()
