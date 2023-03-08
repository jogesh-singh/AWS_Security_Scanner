from boto3 import client
import logging

def encrypt_volume(aws_acceess_key,aws_secret_key,regions):
    logging.info("encrypt_volume called")
    try:
        result=[]
        for region in regions:
            response = client('ec2', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            vol = response.describe_volumes()
            vol_list=[ volume["VolumeId"] for volume in vol["Volumes"] if volume["Encrypted"] == False]
            if vol_list:
                result.append({"Service":"EC2","Issue":"Volumes Not Encrypted","Region":region,"Resources":vol_list})
        return result
    except Exception as e:
        logging.error(f"Volume Error: {e}")
        result=[{"Service":"EC2","Error":e}]
        return result 
