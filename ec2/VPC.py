from json import dumps
from boto3 import client
import logging
def vpc_flow(aws_acceess_key,aws_secret_key,regions):
    logging.info("vpc_flow called")
    try:
        vpc_list=cloudwatch_list={}
        for region in regions:
            response = client('ec2', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            vpc_ids= [vpc["VpcId"] for vpc in response.describe_vpcs()['Vpcs'] ]
            vpcs=cloudwatch=[]
            for id in vpc_ids:
                flow_list = response.describe_flow_logs(Filters=[{"Name":"resource-id","Values":[id]}])
                if not flow_list["FlowLogs"]:
                    vpcs.append(id)
                else:
                    for flow in flow_list["FlowLogs"]:
                        if flow["LogDestinationType"] != "cloud-watch-logs":
                            cloudwatch.append(id)
            if cloudwatch:
                cloudwatch_list[region]=cloudwatch
            if vpcs:
                vpc_list[region]=vpcs
        return dumps({"Flow logs disabled":vpc_list,"cloudwatch logs disabled":cloudwatch_list})
    except Exception as e:
        logging.error(f"VPC Error: {e}")
        return "Error Scanning VPC"