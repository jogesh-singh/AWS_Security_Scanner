from json import dumps
from boto3 import client
import logging
def vpc_flow(aws_acceess_key,aws_secret_key,regions):
    logging.info("vpc_flow called")
    try:
        result=[]
        for region in regions:
            response = client('ec2', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            vpc_ids= [vpc["VpcId"] for vpc in response.describe_vpcs()['Vpcs'] ]
            vpcs=[]
            cloudwatch=[]
            for id in vpc_ids:
                flow_list = response.describe_flow_logs(Filters=[{"Name":"resource-id","Values":[id]}])
                if not flow_list["FlowLogs"]:
                    vpcs.append(id)
                else:
                    for flow in flow_list["FlowLogs"]:
                        if flow["LogDestinationType"] != "cloud-watch-logs":
                            cloudwatch.append(id)
            if vpcs:
                result.append({"Service":"VPC","Issue":"Flow logs disabled","Region":region,"Resources":vpcs})
            if cloudwatch:
                result.append({"Service":"VPC","Issue":"Cloudwatch logs disabled","Region":region,"Resources":cloudwatch})

        return result
    except Exception as e:
        logging.error(f"VPC Error: {e}")
        result=[{"Service":"VPC","Error":e}]
        return result