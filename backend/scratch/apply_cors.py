import boto3
from botocore.exceptions import ClientError

def set_s3_cors(profile_name, bucket_name):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    
    cors_configuration = {
        'CORSRules': [
            {
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'PUT', 'POST', 'HEAD'],
                'AllowedOrigins': ['https://attiquedesign.com', 'http://localhost:5173'],
                'ExposeHeaders': ['ETag', 'Content-Length', 'Content-Type'],
                'MaxAgeSeconds': 3000
            }
        ]
    }
    
    try:
        s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)
        print(f"Successfully updated CORS for {bucket_name} using profile {profile_name}")
    except ClientError as e:
        print(f"Error setting CORS: {e}")

if __name__ == "__main__":
    set_s3_cors('attiquedesign', 'attiquedesign.com')
