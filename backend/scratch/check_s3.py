import boto3
import json
from botocore.exceptions import ClientError

def check_s3_config(bucket_name):
    s3 = boto3.client('s3')
    
    print(f"--- Checking Bucket: {bucket_name} ---")
    
    # 1. CORS
    try:
        cors = s3.get_bucket_cors(Bucket=bucket_name)
        print("CORS Configuration:")
        print(json.dumps(cors.get('CORSRules', []), indent=2))
    except ClientError as e:
        print(f"Error getting CORS: {e}")

    # 2. Bucket Policy
    try:
        policy = s3.get_bucket_policy(Bucket=bucket_name)
        print("\nBucket Policy:")
        print(json.dumps(json.loads(policy.get('Policy', '{}')), indent=2))
    except ClientError as e:
        print(f"\nError getting Policy: {e}")

    # 3. Public Access Block
    try:
        pab = s3.get_public_access_block(Bucket=bucket_name)
        print("\nPublic Access Block:")
        print(json.dumps(pab.get('PublicAccessBlockConfiguration', {}), indent=2))
    except ClientError as e:
        print(f"\nError getting Public Access Block: {e}")

if __name__ == "__main__":
    check_s3_config('attiquedesign.com')
