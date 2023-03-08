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
        if support == False:
            result = [{"Service":"IAM","Issue":"Support Rule Doesn't exist","Region":"Global","Resources":"-"}]
        else:
            result=[]
        return result
    except Exception as e:
        logging.error(f"IAM Support Error: {e}")
        result=[{"Service":"IAM","Error":e}]
        return result
