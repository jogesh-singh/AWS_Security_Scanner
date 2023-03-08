from boto3 import client
from json import dumps
import logging

def config(aws_acceess_key,aws_secret_key,regions):
    logging.info("config called")
    try:
        configs_disabed=[]
        result=[]
        for region in regions:
            response = client('config', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            conigs = response.describe_config_rules()
            if not conigs["ConfigRules"]:
                configs_disabed.append(region)
        if configs_disabed:
            result.append({"Service":"CONFIG","Issue":"Config_disabled","Region":"-","Resources":configs_disabed})
        return result
    except Exception as e:
        logging.error("Config Error: ",e)
        result=[{"Service":"CONFIG","Error":e}]
        return result