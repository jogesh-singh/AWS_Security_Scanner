import pandas,logging
from datetime import datetime
from boto3 import client

def generate_excel_file(result,aws_acceess_key,aws_secret_key):
    try:
        services = []
        Issues = []
        Region = []
        Resource = []

        for i in result:
            if type(result[i]) == dict and len(result[i]) != 0:
                for j in result[i]:
                    if type(result[i][j]) == dict and len(result[i][j]) != 0:
                        for l in result[i][j]:
                            if type(result[i][j][l]) == list and len(result[i][j][l]) != 0:
                                if i == "IAM":
                                    services.append(i)
                                    Issues.append(l)
                                    Region.append("")
                                    Resource.append(f'{result[i][j][l]}')
                                else:
                                    services.append(i)
                                    Issues.append(j)
                                    Region.append(l)
                                    Resource.append(f'{result[i][j][l]}')
                            elif type(result[i][j][l]) == bool:
                                services.append(i)
                                Issues.append(l)
                                Region.append("")
                                Resource.append(f'{result[i][j][l]}')
                    elif type(result[i][j]) == list and len(result[i][j]) != 0:
                        if i == "S3":
                            services.append(i)
                            Issues.append(j)
                            Region.append("Global")
                            Resource.append(f'{result[i][j]}')
                        else:
                            services.append(i)
                            Issues.append(j)
                            Region.append(f'{result[i][j]}')
                            Resource.append("")
                    elif type(result[i][j]) == bool:
                        if j == "Support" and result[i][j] == False:
                            services.append(i)
                            Issues.append(j)
                            Region.append("")
                            Resource.append(f'{result[i][j]}')

        new_dict2 = {"Services": services, "Issues": Issues,
                     "Region": Region, "Resource": Resource}
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