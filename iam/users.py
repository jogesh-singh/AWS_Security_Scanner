import datetime,time,json
from boto3 import client
import logging

def users_detail(aws_acceess_key,aws_secret_key):
    logging.info("users_detail called")
    try:
        iam = client('iam',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)

        report = iam.generate_credential_report()
        time.sleep(5)
        response = iam.get_credential_report()
        report_list=[i.split(',') for i in str(response['Content']).split('\\n')]

        headers = report_list[0]
        report_list.pop(0)

        report_json={}
        count=0
        for i in report_list:
            count+=1
            report_json[count]=dict(zip(headers,i))

        result=[]
        #IAM root user should not be used
        if report_json[1]["access_key_1_active"] == "true" or report_json[1]["access_key_2_active"] == "true":
            result.append({"Service":"IAM","Issue":"Root Users keys are active","Region":"Global","Resources":"-"})

        # #IAM root user MFA not active
        if report_json[1]["mfa_active"] == "true":
            result.append({"Service":"IAM","Issue":"Root Users MFA not Enabled","Region":"Global","Resources":"-"})

        password_age=[]
        today = datetime.datetime.today().date()    
        for i in report_json:
            if report_json[i]["password_last_changed"] != "not_supported" and report_json[i]["password_last_changed"] != "N/A":
                date = datetime.datetime.strptime(report_json[i]["password_last_changed"],'%Y-%m-%dT%H:%M:%S%z').date()
                diff = (today-date).days    
                if diff >= 90:  
                    password_age.append(report_json[i]["b'user"])

        if password_age:
            result.append({"Service":"IAM","Issue":"User with password age more than 90 days","Region":"Global","Resources":password_age})

        users_mfa=[report_json[i]["b'user"] for i in report_json if report_json[i]["password_enabled"] == "true" if report_json[i]["mfa_active"] != "true" ]
        if users_mfa:
            result.append({"Service":"IAM","Issue":"Users with mfa not enabled","Region":"Global","Resources":users_mfa})

        both_keys_active=[report_json[i]["b'user"] for i in report_json if report_json[i]["access_key_1_active"] == "true" and report_json[i]["access_key_2_active"] == "true" ]
        if both_keys_active:
            result.append({"Service":"IAM","Issue":"Users with both keys active","Region":"Global","Resources":both_keys_active})

        return result
    except Exception as e:
        logging.error(f"IAM Users Error: {e}")
        result=[{"Service":"IAM","Error":e}]
        return result
