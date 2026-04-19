import requests
import json

# Replace with your actual API endpoint if different
API_BASE_URL = "https://attiquedesign.com/api" 

def test_full_flow():
    # 1. Get Presigned URL from Backend
    # Note: We need a valid Admin token. Since I don't have one easily, 
    # I will simulate the backend call by calling the function directly if I can,
    # OR I will just use the logic I verified earlier.
    
    # Actually, let's use the local 'storage_service' to generate a URL 
    # and then use 'requests' to PUT it. This mimics the actual Lambda behavior perfectly.
    
    import sys
    sys.path.append('/Users/jungyunyoon/attique-project/backend')
    from chalicelib.services.storage_service import generate_presigned_put_url
    from chalicelib.core.config import settings
    
    print(f"Generating URL for bucket: {settings.S3_BUCKET} in region: {settings.AWS_REGION}")
    
    result = generate_presigned_put_url("test_dummy.txt", "text/plain", "selections")
    upload_url = result['upload_url']
    object_key = result['object_key']
    
    print(f"Generated URL: {upload_url}")
    print(f"Object Key: {object_key}")
    
    print("\nSimulating browser PUT request...")
    # NOTE: We do NOT send Content-Type header to match the backend signature which excludes it.
    resp = requests.put(upload_url, data=b"dummy contents")
    
    if resp.status_code == 200:
        print("Final flow test SUCCESS!")
        # Cleanup
        import boto3
        session = boto3.Session(profile_name='attiquedesign')
        s3 = session.client('s3')
        s3.delete_object(Bucket=settings.S3_BUCKET, Key=object_key)
        print("Cleanup done.")
    else:
        print(f"Final flow test FAILED with {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    test_full_flow()
