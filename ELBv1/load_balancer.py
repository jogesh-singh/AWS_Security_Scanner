from json import dumps
from boto3 import client
import logging

def lb(aws_acceess_key,aws_secret_key,regions):
    logging.info("lb called")
    try:
        lbs={}
        cross_zone={}
        access_log={}
        for region in regions:
            response = client('elb', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            elb = response.describe_load_balancers()
            listners=[]
            lb_names=[]
            cross=[]
            access=[]
            for lb in elb["LoadBalancerDescriptions"]:
                # print("lb result",lb_names)
                lb_names.append(lb["LoadBalancerName"])
                for listner in lb["ListenerDescriptions"]:
                    if listner["Listener"]["LoadBalancerPort"] == 80:
                        listners.append(lb["LoadBalancerName"])
            for name in lb_names:
                elb=response.describe_load_balancer_attributes(LoadBalancerName=name)
                if elb["LoadBalancerAttributes"]["CrossZoneLoadBalancing"]["Enabled"] == False:
                    cross.append(name)
                if elb["LoadBalancerAttributes"]["AccessLog"]["Enabled"] == False:
                    access.append(name)
            if cross:
                cross_zone[region]=cross
            if access:
                access_log[region]=access
            if listners:
                lbs[region]=listners
        return dumps({"Load balancers listening on port 80":lbs,"Cross Zone not enabled":cross_zone,"Access logs not enabled":access_log})
    except Exception as e:
        logging.error(f"Load balancer Error: {e}")
        return "Error Scanning Load Balancers"