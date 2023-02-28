import boto3

def policies_attached_to_users(aws_acceess_key,aws_secret_key):
    print("policies_attached_to_users called")
    iam = boto3.client('iam',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
    response = iam.list_users()
    users=[]
    for user in response["Users"]:
        response = iam.list_attached_user_policies(UserName=user["UserName"])
        if response["AttachedPolicies"]:
            users.append(user["UserName"])
        else:
            response = iam.list_user_policies(UserName=user["UserName"])
            if response["PolicyNames"]:
                users.append(user["UserName"])
    if users:
        return users
    else:
        return 'N/A'

