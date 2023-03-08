from json import dumps
from botocore.exceptions import ClientError
from boto3 import client
import logging

def check_bucket(aws_acceess_key,aws_secret_key):
    logging.info("check_bucket called")
    result=[]
    try:
        s3 = client('s3',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
        s3_buckets = [buckets['Name'] for buckets in s3.list_buckets()["Buckets"]]
        not_encrypted = []
        no_https_policy = []
        logging_disabled=[]
        for bucket in s3_buckets:
            try:
                response = s3.get_bucket_encryption(Bucket=bucket)
            except ClientError as e:
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    not_encrypted.append(bucket)
            try:
                response = s3.get_bucket_policy(Bucket=bucket)
                if "aws:SecureTransport" not in response["Policy"]:
                    no_https_policy.append(bucket)
            except:
                no_https_policy.append(bucket)
            try:
                response = s3.get_bucket_logging(Bucket=bucket)
                if not response.get("LoggingEnabled"):
                    logging_disabled.append(bucket)
            except:
                pass
        if not_encrypted:
            result.append({"Service":"S3","Issue":"Not encrypted","Region":"Global","Resources":not_encrypted})
        if no_https_policy:
            result.append({"Service":"S3","Issue":"No Policy To Only Allow HTTPS Requests","Region":"Global","Resources":no_https_policy})
        if logging_disabled:
            result.append({"Service":"S3","Issue":"Logging Disabled","Region":"Global","Resources":logging_disabled})
        
        return dumps({"Result":result,"Logging Disabled":logging_disabled})
    except Exception as e:
        logging.error(f"S3 Error: {e}")
        result=[{"Service":"S3","Error":e}]
        return result      

