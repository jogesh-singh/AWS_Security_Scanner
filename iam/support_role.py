import boto3
import logging

def support_role(aws_acceess_key,aws_secret_key):
    logging.info("support_role called")
    try:
        support=False
        iam = boto3.client('iam',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
        response=iam.list_roles()
        for role in response["Roles"]:
            if role["Path"] == "/aws-service-role/support.amazonaws.com/":
                support=True
                break
        return support
    except Exception as e:
        logging.error(f"IAM Support Error: {e}")
        return "Error Scanning IAM Support"
