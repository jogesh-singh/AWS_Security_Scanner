import boto3,logging

def Password_Policy(aws_acceess_key,aws_secret_key):
    logging.info("Password_Policy called")
    iam = boto3.client('iam',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
    result=[]

    try:
        response = iam.get_account_password_policy()
        if response["PasswordPolicy"]["MinimumPasswordLength"] < 14:
            result.append({"Service":"IAM","Issue":"Password length policy is less than 14","Region":"Global","Resources":"-"})
        if response["PasswordPolicy"]["PasswordReusePrevention"] < 24:
            result.append({"Service":"IAM","Issue":"Password Reuse policy is less than 24","Region":"Global","Resources":"-"})
        if response["PasswordPolicy"]["RequireSymbols"] != True:
            result.append({"Service":"IAM","Issue":"Password policy doesn't have symbols","Region":"Global","Resources":"-"})
        if response["PasswordPolicy"]["RequireNumbers"] != True:
            result.append({"Service":"IAM","Issue":"Password policy doesn't have numbers","Region":"Global","Resources":"-"})
        if response["PasswordPolicy"]["RequireUppercaseCharacters"] != True:
            result.append({"Service":"IAM","Issue":"Password policy doesn't have Uppercase character","Region":"Global","Resources":"-"})
        if response["PasswordPolicy"]["RequireLowercaseCharacters"] != True:
            result.append({"Service":"IAM","Issue":"Password policy doesn't have Lowercase character","Region":"Global","Resources":"-"})
        if response["PasswordPolicy"]["ExpirePasswords"] != True:
            result.append({"Service":"IAM","Issue":"Password expiration policy is not enabled","Region":"Global","Resources":"-"})
        else:
            if response["PasswordPolicy"]["MaxPasswordAge"] > 90:
                result.append({"Service":"IAM","Issue":"Password age policy is greater than 90 days","Region":"Global","Resources":"-"})
        return result
    except iam.exceptions.NoSuchEntityException:
        result.append({"Service":"IAM","Issue":"No custom password policy","Region":"Global","Resources":"-"})
        return result
    except Exception as e:
        logging.error(f"IAM Password Error: {e}")
        result=[{"Service":"IAM","Error":e}]
        return result