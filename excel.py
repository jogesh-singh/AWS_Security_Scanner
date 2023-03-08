import pandas,logging
from datetime import datetime
from boto3 import client

def generate_excel_file(result,aws_acceess_key,aws_secret_key):
    try:
        services = []
        Issues = []
        Region = []
        Resource = []
        for items in result:
            services.append(items["Service"])
            Issues.append(items["Issue"])
            Region.append(items["Region"])
            if type(items["Resources"]) == list:
                Resource.append(str(items["Resources"])[1:-1].replace("'",""))
            else:
                Resource.append(items["Resources"])

        new_dict2 = {"Services": services, "Issues": Issues, "Region": Region, "Resource": Resource}
        date = datetime.today().date()
        time=datetime.now().strftime("%H:%M:%S")
        Account_ID=client('sts',aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key).get_caller_identity().get('Account')
        pandas.DataFrame(new_dict2).style.set_properties(**{
            'font-family': 'Freesans',
            'font-size': '10pt',
        }).to_excel(f"Security_report_{Account_ID}_{date}_{time}.xlsx", index=False)

        return f"Security_report_{Account_ID}_{date}_{time}.xlsx"
    except Exception as e:
        logging.error(f"PDF Generation error: {e}")
        return "Error"