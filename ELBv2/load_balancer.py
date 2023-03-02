from json import dumps
from boto3 import client
import logging

def lbv2(aws_acceess_key,aws_secret_key,regions):
    logging.info("lbv2 called")
    try:
        access_log={}
        for region in regions:
            response = client('elbv2', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            elb = response.describe_load_balancers()
            lb_names=[]
            access=[]
            for lb in elb["LoadBalancers"]:
                lb_names.append(lb["LoadBalancerArn"])
            for name in lb_names:
                elb=response.describe_load_balancer_attributes(LoadBalancerArn=name)
                for attri in elb["Attributes"]:
                    if attri["Key"]=="access_logs.s3.enabled" and attri["Value"] == "false":
                        access.append(name)

            if access:
                access_log[region]=access
        return dumps({"Access logs not enabled":access_log})
    except Exception as e:
        logging.error(f"Load balancer Error: {e}")
        return "Error Scanning Load Balancers"