import boto3
from botocore.exceptions import ClientError

def check_access(profile):
    print(f"--- Checking with profile: {profile} ---")
    session = boto3.Session(profile_name=profile)
    s3 = session.client('s3')
    bucket_name = 'attiquedesign.com'
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Access to {bucket_name}: SUCCESS")
        
        # Try to get cors
        try:
            cors = s3.get_bucket_cors(Bucket=bucket_name)
            print("GET CORS: SUCCESS")
        except:
            print("GET CORS: FAILED")
            
    except ClientError as e:
        print(f"Access to {bucket_name}: FAILED ({e})")

if __name__ == "__main__":
    check_access('default')
    check_access('attiquedesign')
