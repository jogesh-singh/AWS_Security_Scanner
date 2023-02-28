from json import dumps
from botocore.exceptions import ClientError
from boto3 import client

def check_bucket(aws_acceess_key,aws_secret_key):
    print("check_bucket called")
    try:
        s3 = client('s3',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
        s3_buckets = [buckets['Name'] for buckets in s3.list_buckets()["Buckets"]]
        not_encrypted = []
        no_https_policy = []
        logging_disabled=[]
        # print(s3_buckets)
        for bucket in s3_buckets:
            # print(bucket)
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
        return dumps({"Not encrypted":not_encrypted,"No Policy To Only Allow HTTPS Requests":no_https_policy,"Logging Disabled":logging_disabled})
    except Exception as e:
        print("S3 Error: ",e)
        return "Error Scanning S3"       

