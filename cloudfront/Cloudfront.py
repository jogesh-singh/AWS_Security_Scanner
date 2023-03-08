from json import dumps
import boto3
import logging

def cloudfront_scan(aws_acceess_key,aws_secret_key):
    logging.info("Cloudfront scan called")
    result=[]
    try:
        origin=[]
        viewer=[]
        access=[]
        cloudfront = boto3.client('cloudfront',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
        response = cloudfront.list_distributions()
        dist_ids=[]
        if response["DistributionList"].get("Items"):
            for distribution in response["DistributionList"]["Items"]:
                dist_ids.append(distribution['Id'])
                for origins in distribution["Origins"]["Items"]:
                    if origins.get("CustomOriginConfig"):
                        if origins["CustomOriginConfig"]["OriginProtocolPolicy"] != "https-only":
                            origin.append(distribution['Id'])
                if distribution["DefaultCacheBehavior"]["ViewerProtocolPolicy"] != "redirect-to-https" or distribution["DefaultCacheBehavior"]["ViewerProtocolPolicy"] != "https-only":
                    viewer.append(distribution['Id'])
        
        for id in dist_ids:
            response = cloudfront.get_distribution(Id=id)
            if response["Distribution"]["DistributionConfig"]["Logging"]["Enabled"] == False:
                access.append(id)

        if origin:
            result.append({"Service":"CLOUDFRONT","Issue":"Distributions without origin policy set to https-only","Region":"Global","Resources":origin})

        if access:
            result.append({"Service":"CLOUDFRONT","Issue":"Access logging disabled","Region":"Global","Resources":access})

        if viewer:
            result.append({"Service":"CLOUDFRONT","Issue":"Distributions without viewer policy set to https-only or redirect-to-https","Region":"Global","Resources":viewer})
        return result
    except Exception as e:
        logging.error(f"Cloudfront Error: {e}")
        result=[{"Service":"CLOUDFRONT","Error":e}]
        return result
