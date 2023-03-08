from json import dumps
from boto3 import client
import logging

def lbv2(aws_acceess_key,aws_secret_key,regions):
    logging.info("lbv2 called")
    try:
        result=[]
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
                result.append({"Service":"ELBv2","Issue":"Access logs not enabled","Region":region,"Resources":access})
        return result
    except Exception as e:
        logging.error(f"Load balancer Error: {e}")
        result=[{"Service":"ELBv2","Error":e}]
        return result