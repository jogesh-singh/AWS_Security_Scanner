from boto3 import client
import logging

def auto_scale(aws_acceess_key,aws_secret_key,regions):
    logging.info("auto scale called")
    try:
        result=[]
        for region in regions:
            response = client('autoscaling', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            auto_scaleing = response.describe_auto_scaling_groups()
            scaling=[groups["AutoScalingGroupName"] for groups in auto_scaleing["AutoScalingGroups"] if len(groups["AvailabilityZones"]) < 2 ]
            if scaling:
                result.append({"Service":"AOTO SCALING","Issue":"Avaliability zones are less than 2","Region":region,"Resources":scaling})     
        return result
    except Exception as e:
        logging.error(f"AutoScale Error: {e}")
        result=[{"Service":"AOTO SCALING","Error":e}]
        return result