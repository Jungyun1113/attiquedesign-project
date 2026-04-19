import boto3
import subprocess
import os

# 1. Chalice package 생성
print("Packaging chalice app...")
subprocess.run(["chalice", "package", "out/"], check=True)

# 2. Boto3로 Lambda 코드 업데이트
lambda_client = boto3.client('lambda', region_name='ap-northeast-2')
function_name = 'attique-project-prod'
zip_file_path = 'out/deployment.zip'

with open(zip_file_path, 'rb') as f:
    zipped_code = f.read()

print(f"Updating lambda function: {function_name}...")
response = lambda_client.update_function_code(
    FunctionName=function_name,
    ZipFile=zipped_code
)

print("Lambda update response:", response['LastUpdateStatus'])
if response['LastUpdateStatus'] == 'Successful':
    print("SUCCESS: Lambda code updated directly!")
else:
    print("FAILED: Lambda update not successful.")
