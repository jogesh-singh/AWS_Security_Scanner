from boto3 import client
import logging
def open_traffic(aws_acceess_key,aws_secret_key,regions):
    logging.info("open_traffic called")
    try:
        security_groups={"all_traffic_open":{},"open_ports_22":{},"open_ports_23":{},"open_ports_3306":{}}
        for region in regions:
            sg = client('ec2', region_name=region,aws_access_key_id=aws_acceess_key,aws_secret_access_key=aws_secret_key)
            SG = sg.describe_security_groups()
            # ports_list=[22,5000,5900,5800,23,3306]
            all_traffic=[]
            open_ports_22=[]
            open_ports_23=[]
            open_ports_3306=[]
            for groups in SG["SecurityGroups"]:
                for permissions in groups["IpPermissions"]:
                    for CIDR in permissions["IpRanges"]:
                        if CIDR["CidrIp"] == "0.0.0.0/0":
                            if permissions["IpProtocol"] == "-1":
                                all_traffic.append(groups["GroupId"])
                            else:
                                if permissions.get("FromPort") or permissions.get("ToPort"):
                                    if permissions["FromPort"] == 22 or permissions["ToPort"] == 22:
                                        open_ports_22.append([groups["GroupId"]])
                                    if permissions["FromPort"] == 23 or permissions["ToPort"] == 23:
                                        open_ports_23.append([groups["GroupId"]])
                                    if permissions["FromPort"] == 3306 or permissions["ToPort"] == 3306:
                                        open_ports_3306.append([groups["GroupId"]])

            if all_traffic:
                security_groups["All Traffic Open"]={}
                security_groups["All Traffic Open"][region]=all_traffic
            if open_ports_22:
                security_groups["Port 22 is open"]={}
                security_groups["Port 22 is open"][region]=open_ports_22
            if open_ports_23:
                security_groups["Port 23 is open"]={}
                security_groups["Port 23 is open"][region]=open_ports_23
            if open_ports_3306:
                security_groups["Port 3306 is open"]={}
                security_groups["Port 3306 is open"][region]=open_ports_3306

        return security_groups
    except Exception as e:
        logging.error(f"EC2 Security Groups Error: {e}")
        return "Error Scanning Security Groups"
