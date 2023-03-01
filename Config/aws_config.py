from boto3 import client
from json import dumps
import logging

def config(aws_acceess_key,aws_secret_key,regions):
    logging.info("config called")
    try:
        configs_disabed=[]
        for region in regions:
            response = client('config', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            conigs = response.describe_config_rules()
            if not conigs["ConfigRules"]:
                configs_disabed.append(region)
        return dumps({"Config_disabled":configs_disabed})
    except Exception as e:
        logging.error("Config Error: ",e)
        return "Error Scanning Config"
