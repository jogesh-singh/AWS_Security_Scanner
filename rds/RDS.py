from json import dumps
from boto3 import client
import logging

def check_rds(aws_acceess_key,aws_secret_key,regions):
    logging.info("check_rds called")
    result=[]
    try: 
        for region in regions:
            multi_az=[]
            delete_protect=[]
            enhance_monitor=[]
            rds = client('rds', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            response = rds.describe_db_instances()
            for DB in response["DBInstances"]:
                if DB["MultiAZ"] == False:
                    multi_az.append(DB["DBInstanceIdentifier"])
                if DB["DeletionProtection"] == False:
                    delete_protect.append(DB["DBInstanceIdentifier"])
                if not DB.get("EnhancedMonitoringResourceArn"):
                    enhance_monitor.append(DB["DBInstanceIdentifier"])
            if multi_az:
                result.append({"Service":"RDS","Issue":"Multi AZ disabled","Region":region,"Resources":multi_az})
            if delete_protect:
                result.append({"Service":"RDS","Issue":"Delete Protection Disabled","Region":region,"Resources":delete_protect})
            if enhance_monitor:
                result.append({"Service":"RDS","Issue":"Enhanced monitoring disabled","Region":region,"Resources":enhance_monitor})
        return result
    except Exception as e:
        logging.error(f"RDS Error: {e}")
        result=[{"Service":"RDS","Error":e}]
        return result 


