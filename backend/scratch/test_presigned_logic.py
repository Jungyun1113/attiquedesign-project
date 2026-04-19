import boto3
import requests
from botocore.config import Config
import os

def test_presigned_url_logic(profile_name, bucket_name):
    # Mimic storage_service.py logic
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client(
        "s3",
        region_name="ap-northeast-2",
        config=Config(
            s3={"addressing_style": "path"},
            signature_version="s3v4"
        ),
    )
    
    object_key = "test_logic/dummy.txt"
    
    print(f"Generating presigned URL for {object_key}...")
    url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_key,
        },
        ExpiresIn=300
    )
    print(f"URL: {url}")
    
    print("\nAttempting PUT request via requests library (no content-type)...")
    content = b"test content"
    resp = requests.put(url, data=content)
    
    if resp.status_code == 200:
        print("PUT SUCCESS!")
    else:
        print(f"PUT FAILED with status {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    test_presigned_url_logic('attiquedesign', 'attiquedesign.com')
