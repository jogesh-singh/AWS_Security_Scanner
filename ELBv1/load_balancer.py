from json import dumps
from boto3 import client
import logging

def lb(aws_acceess_key,aws_secret_key,regions):
    logging.info("lb called")
    try:
        result=[]
        for region in regions:
            response = client('elb', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            elb = response.describe_load_balancers()
            listners=[]
            lb_names=[]
            cross=[]
            access=[]
            for lb in elb["LoadBalancerDescriptions"]:
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
                result.append({"Service":"ELBv1","Issue":"Cross Zone not enabled","Region":region,"Resources":cross})
            if access:
                result.append({"Service":"ELBv1","Issue":"Access logs not enabled","Region":region,"Resources":access})
            if listners:
                result.append({"Service":"ELBv1","Issue":"Load balancers listening on port 80","Region":region,"Resources":listners})

        return result
    except Exception as e:
        logging.error(f"Load balancer Error: {e}")
        result=[{"Service":"ELBv1","Error":e}]
        return result