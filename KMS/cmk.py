from json import dumps
from boto3 import client
import logging

def cmk_rotate(aws_acceess_key,aws_secret_key):
    logging.info("kms called")
    try:
        kms=client('kms',region_name="us-west-2",aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
        response = kms.list_aliases()
        keys_list=[keys["TargetKeyId"] for keys in response["Aliases"] if not 'alias/aws' in keys["AliasName"] if keys.get("TargetKeyId")]
        rotate_status=[]
        for key in keys_list:
            response = kms.get_key_rotation_status(KeyId=key)
            if response["KeyRotationEnabled"] == False:
                rotate_status.append(key)
        result=[{"Service":"KMS","Issue":"Keys not Rotated","Region":"Global","Resources":rotate_status}]
        return result
    except Exception as e:
        logging.error(f"KMS Error: {e}")
        result=[{"Service":"KMS","Error":e}]
        return result
