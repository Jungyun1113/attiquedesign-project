import boto3

def upload_packaged_zip(profile_name, function_name, zip_path):
    session = boto3.Session(profile_name=profile_name)
    client = session.client('lambda', region_name='ap-northeast-2')
    
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    print(f"Uploading {zip_path} to lambda: {function_name}...")
    try:
        response = client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        print(f"Success! LastModified: {response['LastModified']}")
        print(f"CodeSha256: {response['CodeSha256']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    upload_packaged_zip('attiquedesign', 'attique-project-prod', '/Users/jungyunyoon/attique-project/backend/out/deployment.zip')
