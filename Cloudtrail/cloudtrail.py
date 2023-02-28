from json import dumps
from boto3 import client

def cloud_trail(aws_acceess_key,aws_secret_key,regions,logging_disabled):
    print("Cloudtrail called")
    try:
        log_file_validation={}
        cloudwatch_logs={}
        encryption={}
        s3_buckets=[]
        trails_disabed=[]
        for region in regions:
            response = client('cloudtrail', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            trails = response.describe_trails()
            if not trails["trailList"]:
                trails_disabed.append(region)
            else:
                [s3_buckets.append(trail["S3BucketName"]) for trail in trails["trailList"] if trail["S3BucketName"] not in s3_buckets ]
                validation=[trail["Name"] for trail in trails["trailList"] if trail["LogFileValidationEnabled"] == False]
                cloudwatch=[trail["Name"] for trail in trails["trailList"] if not trail.get("CloudWatchLogsRoleArn")]
                encrypt=[trail["Name"] for trail in trails["trailList"] if not trail.get("KmsKeyId")]
                if validation:
                    log_file_validation[region] = validation
                if cloudwatch:
                    cloudwatch_logs[region] = cloudwatch
                if encrypt:
                	encryption[region]=encrypt
        if s3_buckets:
            ACL = acl_check(aws_acceess_key,aws_secret_key,s3_buckets)
            logging_disabled_cloudtrail_buckets=[bucket for bucket in s3_buckets if bucket in logging_disabled]
        else:
            logging_disabled_cloudtrail_buckets={}
            ACL         = {}
        return dumps({
            "Trails_disabled":trails_disabed,
            "Encryption Disabled":encryption,
            "Log file validation Disbaled":log_file_validation,
            "Cloudwatch logs Disabled":cloudwatch_logs,
            "ACL" :ACL,
            "Cloudtrail bucket loggin disabled":logging_disabled_cloudtrail_buckets
        })
    except Exception as e:
        print("Cloudtrail Error: ",e)
        return "Error Scanning Cloudtrail"

def acl_check(aws_acceess_key,aws_secret_key,trail_buckets):
    print("acl check called")
    acl_list=[]
    s3=client('s3',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
    for bucket in trail_buckets:
        print(bucket)
        try:
            response=s3.get_bucket_acl(Bucket=bucket)
            for grant in response["Grants"]:
                if grant["Grantee"].get("URI"):
                    if "AllUsers" in grant["Grantee"]["URI"] or "AuthenticatedUsers" in grant["Grantee"]["URI"]:
                        acl_list.append(bucket)
        except Exception as e:
            print(e)
    return acl_list
