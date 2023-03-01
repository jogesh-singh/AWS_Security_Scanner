from boto3 import client
import logging

def auto_scale(aws_acceess_key,aws_secret_key,regions):
    logging.info("auto scale called")
    try:
        auto_scaling={}
        for region in regions:
            response = client('autoscaling', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            auto_scaleing = response.describe_auto_scaling_groups()

            scaling=[groups["AutoScalingGroupName"] for groups in auto_scaleing["AutoScalingGroups"] if len(groups["AvailabilityZones"]) < 2 ]
            if scaling:
                auto_scaling[region]=scaling
        return auto_scaling
    except Exception as e:
        logging.error(f"AutoScale Error: {e}")
        return "Error Scanning AutoScale"