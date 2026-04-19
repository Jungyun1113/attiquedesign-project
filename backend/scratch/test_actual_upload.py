import boto3
from botocore.exceptions import ClientError

def test_actual_upload(profile_name, bucket_name):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    try:
        print(f"Testing upload to {bucket_name} using profile {profile_name}...")
        s3.put_object(Bucket=bucket_name, Key='test_upload_from_script.txt', Body='hello world')
        print("Upload: SUCCESS")
        s3.delete_object(Bucket=bucket_name, Key='test_upload_from_script.txt')
        print("Delete: SUCCESS")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_actual_upload('attiquedesign', 'attiquedesign.com')
