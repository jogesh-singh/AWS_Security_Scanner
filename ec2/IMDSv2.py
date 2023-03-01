import boto3,logging
def imdsv2(aws_acceess_key,aws_secret_key,regions):
    logging.info("imdsv2 called")
    try:
        result={}
        for region in regions:
            response = boto3.client('ec2', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            ec2 = response.describe_instances()
            if ec2["Reservations"]:
                v2=[instance["Instances"][0]["InstanceId"] for instance in ec2["Reservations"] if instance["Instances"][0]["MetadataOptions"]["HttpTokens"] == "optional"]
                result[region] = v2
        return result
    except Exception as e:
        logging.error(f"EC2 IMDSv2 Error: {e}")
        return "Error Scanning EC2 IMDSv2"




