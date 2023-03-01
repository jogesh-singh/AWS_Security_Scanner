import boto3
from botocore.exceptions import ClientError
import logging

def create_session(aws_acceess_key,aws_secret_key):
    try:
        client = boto3.client('ec2', region_name='us-west-1',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)

        regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
        return regions
    except ClientError as e:
        Error = e.response['Error']['Code']
        logging.error(Error)
        return Error