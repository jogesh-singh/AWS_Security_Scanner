from json import dumps
import boto3

def cloudfront_scan(aws_acceess_key,aws_secret_key):
    print("Cloudfront scan called")
    result={}
    try:
        origin=[]
        viewer=[]
        cloudfront = boto3.client('cloudfront',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
        response = cloudfront.list_distributions()
        if response["DistributionList"].get("Items"):
            for distribution in response["DistributionList"]["Items"]:
                for origins in distribution["Origins"]["Items"]:
                    if origins.get("CustomOriginConfig"):
                        if origins["CustomOriginConfig"]["OriginProtocolPolicy"] != "https-only":
                            origin.append(distribution['Id'])
                if distribution["DefaultCacheBehavior"]["ViewerProtocolPolicy"] != "redirect-to-https" or distribution["DefaultCacheBehavior"]["ViewerProtocolPolicy"] != "https-only":
                    viewer.append(distribution['Id'])
        if origin:
            result["Distributions without origin policy set to https-only"]=origin
        if viewer:
            result["Distributions without viewer policy set to https-only or redirect-to-https"]=viewer
        return result
    except Exception as e:
        print("Cloudfront Error: ",e)
        return "Error Scanning Cloudfront"
