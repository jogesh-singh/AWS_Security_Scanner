import boto3

def Password_Policy(aws_acceess_key,aws_secret_key):
    print("Password_Policy called")
    iam = boto3.client('iam',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
    password={}

    try:
        response = iam.get_account_password_policy()
        if response["PasswordPolicy"]["MinimumPasswordLength"] < 14:
            password["Password length policy is less than 14 "]=False
        if response["PasswordPolicy"]["PasswordReusePrevention"] < 24:
            password["Password Reuse policy is less than 24 "] = False
        if response["PasswordPolicy"]["RequireSymbols"] != True:
            password["Symbols are not required in password policy"] = False
        if response["PasswordPolicy"]["RequireNumbers"] != True:
            password["Numbers are not required on password policy"] = False
        if response["PasswordPolicy"]["RequireUppercaseCharacters"] != True:
            password["Uppercase characters are not required in password policy"] = False
        if response["PasswordPolicy"]["RequireLowercaseCharacters"] != True:
            password["Lowercase letters are not required in passowrd policy"] = False
        if response["PasswordPolicy"]["ExpirePasswords"] != True:
            password["Password expiration policy is not enabled"] = False
        else:
            if response["PasswordPolicy"]["MaxPasswordAge"] > 90:
                password["Password age policy is greater than 90 days"] = False
        return password
    except iam.exceptions.NoSuchEntityException:
        password={
            "No Custom Password Policy Used":False
        }
        return password
    except Exception as e:
        print("IAM Password Error: ",e)
        return "Error Scanning IAM Password"