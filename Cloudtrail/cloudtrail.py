from json import dumps
from boto3 import client
import logging

def cloud_trail(aws_acceess_key,aws_secret_key,regions,logging_disabled):
    logging.info("Cloudtrail called")
    try:
        result=[]
        trails_disabed=[]
        for region in regions:
            s3_buckets=[]
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
                    result.append({"Service":"CLOUDTRAIL","Issue":"Log file validation Disbaled","Region":region,"Resources":validation})
                if cloudwatch:
                    result.append({"Service":"CLOUDTRAIL","Issue":"Cloudwatch logs Disabled","Region":region,"Resources":cloudwatch})
                if encrypt:
                    result.append({"Service":"CLOUDTRAIL","Issue":"Encryption Disabled","Region":region,"Resources":encrypt})
                if s3_buckets:
                    ACL = acl_check(aws_acceess_key,aws_secret_key,s3_buckets)
                    logging_disabled_cloudtrail_buckets=[bucket for bucket in s3_buckets if bucket in logging_disabled]

                if logging_disabled_cloudtrail_buckets:
                    result.append({"Service":"CLOUDTRAIL","Issue":"Cloudtrail bucket loggin disabled","Region":region,"Resources":logging_disabled_cloudtrail_buckets})

                if ACL:
                    result.append({"Service":"CLOUDTRAIL","Issue":"ACL","Region":region,"Resources":ACL})
        if trails_disabed:
            result.append({"Service":"CLOUDTRAIL","Issue":"Trails_disabled","Region":"-","Resources":trails_disabed})


        return result
    except Exception as e:
        logging.error(f"Cloudtrail Error: {e}")
        result=[{"Service":"CLOUDTRAIL","Error":e}]
        return result

def acl_check(aws_acceess_key,aws_secret_key,trail_buckets):
    logging.info("acl check called")
    acl_list=[]
    try:
        s3=client('s3',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
        for bucket in trail_buckets:
            try:
                response=s3.get_bucket_acl(Bucket=bucket)
                for grant in response["Grants"]:
                    if grant["Grantee"].get("URI"):
                        if "AllUsers" in grant["Grantee"]["URI"] or "AuthenticatedUsers" in grant["Grantee"]["URI"]:
                            acl_list.append(bucket)
            except Exception as e:
                logging.error(f"ACL Error: {e}")
        return acl_list
    except Exception as e:
        logging.error(f"ACL Error: {e}")
        return acl_list
    
