import boto3

def find_lambda_role_and_policy(profile_name):
    session = boto3.Session(profile_name=profile_name)
    client = session.client('lambda')
    iam = session.client('iam')
    
    try:
        # Assuming the function name contains 'attique'
        functions = client.list_functions()
        target_funcs = [f for f in functions['Functions'] if 'attique' in f['FunctionName']]
        
        for f in target_funcs:
            role_arn = f['Role']
            role_name = role_arn.split('/')[-1]
            print(f"\nLambda Function: {f['FunctionName']}")
            print(f"Role Name: {role_name}")
            
            # List attached policies
            attached = iam.list_attached_role_policies(RoleName=role_name)
            for p in attached['AttachedPolicies']:
                print(f"  - Attached Policy: {p['PolicyName']} ({p['PolicyArn']})")
                
            # List inline policies
            inline = iam.list_role_policies(RoleName=role_name)
            for p_name in inline['PolicyNames']:
                print(f"  - Inline Policy: {p_name}")
                p_detail = iam.get_role_policy(RoleName=role_name, PolicyName=p_name)
                print(p_detail['PolicyDocument'])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_lambda_role_and_policy('attiquedesign')
