from boto3 import client

def encrypt_volume(aws_acceess_key,aws_secret_key,regions):
    print("encrypt_volume called")
    try:
        volumes={}
        for region in regions:
            response = client('ec2', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            vol = response.describe_volumes()
            vol_list=[ volume["VolumeId"] for volume in vol["Volumes"] if volume["Encrypted"] == False]
            if vol_list:
                volumes[region] = vol_list

        return volumes
    except Exception as e:
        print("Volume Error: ",e)
        return "Error Scanning Volumes"
