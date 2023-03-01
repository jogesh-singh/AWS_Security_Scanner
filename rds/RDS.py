from json import dumps
from boto3 import client
import logging

def check_rds(aws_acceess_key,aws_secret_key,regions):
    logging.info("check_rds called")
    try: 
        Multi_AZ_disabled={}
        Delete_Protection_Disabled={}
        Enhanced_monitoring_disabled={}
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
                Multi_AZ_disabled[region]=multi_az
            if delete_protect:
                Delete_Protection_Disabled[region]=delete_protect
            if enhance_monitor:
                Enhanced_monitoring_disabled[region]=enhance_monitor
        return dumps({"Multi AZ disabled":Multi_AZ_disabled,"Delete Protection Disabled":Delete_Protection_Disabled,"Enhanced monitoring disabled":Enhanced_monitoring_disabled})
    except Exception as e:
        logging.error(f"RDS Error: {e}")
        return "Error Scanning RDS"


