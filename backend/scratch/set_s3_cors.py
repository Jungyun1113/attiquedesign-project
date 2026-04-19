import boto3
from botocore.exceptions import ClientError

def set_s3_cors(bucket_name):
    s3 = boto3.client('s3')
    
    cors_configuration = {
        'CORSRules': [
            {
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'PUT', 'POST', 'HEAD'],
                'AllowedOrigins': ['https://attiquedesign.com', 'http://localhost:5173'],
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3000
            }
        ]
    }
    
    try:
        s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)
        print(f"Successfully updated CORS for {bucket_name}")
    except ClientError as e:
        print(f"Error setting CORS: {e}")

if __name__ == "__main__":
    set_s3_cors('attiquedesign.com')
