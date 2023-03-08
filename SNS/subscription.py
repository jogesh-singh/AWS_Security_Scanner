from boto3 import client
from logging import info,error

def sub_check(aws_acceess_key,aws_secret_key,regions):
    try:
        info("Scanning SNS")
        result=[]
        for region in regions:
            sub_id=[]
            sns = client('sns', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            response = sns.list_subscriptions()
            for subs in response["Subscriptions"]:
                if subs["Protocol"] == "http":
                    sub_id.append(subs["SubscriptionArn"])
            if sub_id:
                result.append({"Service":"SNS","Issue":"Subscriptions with HTTP Protocol","Region":region,"Resources":sub_id})
        return result
    except Exception as e:
        error(f"SNS Scan Error: {e}")
        result=[{"Service":"SNS","Error":e}]
        return result

