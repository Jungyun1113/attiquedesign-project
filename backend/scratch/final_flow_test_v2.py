import boto3
import requests
from botocore.config import Config
import os
import sys

# Ensure backend path is in sys.path
sys.path.append('/Users/jungyunyoon/attique-project/backend')

def test_full_flow_with_profile():
    # Force use of attiquedesign profile
    session = boto3.Session(profile_name='attiquedesign')
    
    # We need to manually initialize storage service's client for the test
    # since it normally uses the default session
    s3_client = session.client(
        "s3",
        region_name="ap-northeast-2",
        config=Config(
            s3={"addressing_style": "path"},
            signature_version="s3v4"
        ),
    )
    
    bucket_name = "attiquedesign.com"
    object_key = "selections/test_final.txt"
    
    print(f"Generating URL for bucket: {bucket_name} using attiquedesign profile...")
    
    upload_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_key,
        },
        ExpiresIn=300
    )
    
    print(f"Generated URL: {upload_url}")
    
    print("\nSimulating browser PUT request (via requests)...")
    resp = requests.put(upload_url, data=b"final test")
    
    if resp.status_code == 200:
        print("SUCCESS! The credentials and bucket are now in sync.")
        # Cleanup
        s3_client.delete_object(Bucket=bucket_name, Key=object_key)
        print("Cleanup done.")
    else:
        print(f"FAILED with {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    test_full_flow_with_profile()
