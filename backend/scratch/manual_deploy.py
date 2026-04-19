import boto3
import zipfile
import os
import io

def manual_update_lambda(profile_name, function_name):
    session = boto3.Session(profile_name=profile_name)
    client = session.client('lambda', region_name='ap-northeast-2')
    
    # 1. Zip the current backend directory (excluding .venv, __pycache__, etc)
    mem_file = io.BytesIO()
    with zipfile.ZipFile(mem_file, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk('/Users/jungyunyoon/attique-project/backend'):
            if '.venv' in root or '__pycache__' in root or '.chalice' in root or 'scratch' in root:
                continue
            for file in files:
                if file.endswith('.pyc') or file == '.env':
                    continue
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, '/Users/jungyunyoon/attique-project/backend')
                zf.write(abs_path, rel_path)
    
    mem_file.seek(0)
    
    print(f"Updating code for lambda: {function_name}...")
    try:
        response = client.update_function_code(
            FunctionName=function_name,
            ZipFile=mem_file.read()
        )
        print(f"Success! LastModified: {response['LastModified']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # The prod function name we found earlier
    manual_update_lambda('attiquedesign', 'attique-project-prod')
