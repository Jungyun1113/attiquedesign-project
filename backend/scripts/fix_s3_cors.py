import boto3
import os
from dotenv import load_dotenv

# .env 로드
load_dotenv()

bucket_name = "attiquedesign.com"
region = "ap-northeast-2"

s3 = boto3.client("s3", region_name=region)

cors_configuration = {
    'CORSRules': [
        {
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'DELETE', 'HEAD'],
            'AllowedOrigins': ['*'],  # 모든 도메인 허용 (개발 및 운영 환경 모두 포함)
            'ExposeHeaders': ['ETag'],
            'MaxAgeSeconds': 3000
        }
    ]
}

try:
    print(f"Setting CORS for bucket: {bucket_name}...")
    s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)
    print("CORS configuration applied successfully!")
except Exception as e:
    print(f"Error setting CORS: {e}")
