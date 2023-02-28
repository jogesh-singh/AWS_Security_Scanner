from flask import Flask, request, render_template,send_file, redirect
from threading import Thread
from datetime import datetime
from excel import generate_excel_file
from cloudfront.Cloudfront import cloudfront_scan
from session.Session import create_session
from iam.support_role import support_role
# from iam.user_policy import policies_attached_to_users
from ec2.IMDSv2 import imdsv2
from iam.password_policy import Password_Policy
from rds.RDS import check_rds
from S3.bucket import check_bucket
from iam.users import users_detail
from security_groups.SG import open_traffic
from ec2.Volume import encrypt_volume
from ec2.VPC import vpc_flow
from ELBv1.load_balancer import lb
from AutoScalling.scaling import auto_scale
from Cloudtrail.cloudtrail import cloud_trail  
from Config.aws_config import config
from KMS.cmk import cmk_rotate
from json import loads,dumps

def scan_aws(aws_acceess_key,aws_secret_key,regions):
    global file_name,result
    result={"IAM":{},"EC2":{}}
    result["Cloudfront"] = cloudfront_scan(aws_acceess_key,aws_secret_key)
    # Policy          = policies_attached_to_users(aws_acceess_key,aws_secret_key)
    result["IAM"]["Support"] = support_role(aws_acceess_key,aws_secret_key)
    result["EC2"]["Instances With IMDSv2 Disabled"]          = imdsv2(aws_acceess_key,aws_secret_key,regions)
    result["IAM"]["Password"]        = Password_Policy(aws_acceess_key,aws_secret_key)
    result["RDS"]             = loads(check_rds(aws_acceess_key,aws_secret_key,regions))
    result["S3"]              = loads(check_bucket(aws_acceess_key,aws_secret_key))
    result["SG"]            = open_traffic(aws_acceess_key,aws_secret_key,regions)
    result["IAM"]["Users"]           = users_detail(aws_acceess_key,aws_secret_key)
    result["EC2"]["Volumes Not Encrypted"]         = encrypt_volume(aws_acceess_key,aws_secret_key,regions)
    result["VPC"]       = loads(vpc_flow(aws_acceess_key,aws_secret_key,regions))
    result["ELBv1"]           = loads(lb(aws_acceess_key,aws_secret_key,regions))
    result["AUTO_SCALING"]    = auto_scale(aws_acceess_key,aws_secret_key,regions)
    result["CLOUDTRAIL"]  = loads(cloud_trail(aws_acceess_key,aws_secret_key,regions,result["S3"]["Logging Disabled"]))
    result["CONFIG"]          = loads(config(aws_acceess_key,aws_secret_key,regions))
    result["KMS"]        = cmk_rotate(aws_acceess_key,aws_secret_key)
    print("Scan Completed at ",datetime.now().strftime("%H:%M:%S"))
    print('Generating Excel File')
    file_name = generate_excel_file(result,aws_acceess_key,aws_secret_key)
    print('Excel File Generated')



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan',methods=['GET','POST'])
def scan():
    if request.method == "POST":
        print("Scan Started at ",datetime.now().strftime("%H:%M:%S"))
        access_key = request.form.get("Access_Key")
        secret_key = request.form.get("Secret_Key")
        regions = create_session(access_key,secret_key)
        if regions == "AuthFailure":
            return render_template('index.html', error="Invalid Credentials!")
        else:
            t1 = Thread(target=scan_aws,args=(access_key,secret_key,regions))
            t1.start()
            return render_template('loading.html')
    return redirect('/')

@app.route('/status', methods=['GET'])
def getStatus():
    global result
    status = int((len(result)/12)*100)
    statusList = {'status':status}
    return dumps(statusList)

@app.route('/report',methods=['GET','POST'])
def frontend():
    global file_name,result

    if request.method == "POST":
        print(request.form.get("Filename"))
        return send_file(file_name)
    return render_template('report.html',res=result)

if __name__ == '__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")

    #40 checks
