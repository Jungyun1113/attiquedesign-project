import boto3
from botocore.exceptions import ClientError

def test_upload(bucket_name):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket_name, Key='test_permission_check.txt', Body='test contents')
        print(f"Successfully uploaded to {bucket_name}")
        # Clean up
        s3.delete_object(Bucket=bucket_name, Key='test_permission_check.txt')
        print("Successfully deleted test file")
    except ClientError as e:
        print(f"Error during upload test: {e}")

if __name__ == "__main__":
    test_upload('attiquedesign.com')
