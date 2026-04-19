import boto3
import json
from botocore.exceptions import ClientError

def check_s3_details(profile_name, bucket_name):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    
    print(f"--- Checking Bucket: {bucket_name} with profile {profile_name} ---")
    
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

if __name__ == "__main__":
    check_s3_details('attiquedesign', 'attiquedesign.com')
