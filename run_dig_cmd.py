import subprocess
import shlex
import app_list as wb
from pathlib import Path
import datetime
import difflib
import sys
from itertools import izip
import glob
import os
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import yaml
import wget
import tarfile



#Function to run the dig command using subprocess Popen based on the domain/hostname and Ip address and storing the response(app_id)
#separetly log file for each

def run_cmd(webnip_list,flg):
    if flg=="weblist":
        web_list=webnip_list
        date_time=datetime.datetime.now()
        date_time="/appctrl/t/test/log/domainlog/"+str(date_time)+".log"
        Path(date_time).touch()
        my_file=open(date_time,"w")
        my_file.write("Application-name |Response \n\n")
        for i in range(0,len(web_list)):
            s2="www."+web_list[i]
            s1="dig "
            s3=".80.6.1.2.3.4.v0.appcs.x.riverbed.cc AAAA @pastage.appcs.x.riverbed.cc +short"
            cmd=s1+s2+s3
            proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
            out,err=proc.communicate()
            if(out==''):
                s=web_list[i]+" |"+"No-Response"+"\n"
                my_file.write(s)
                res_flag=True
            else:
                s=web_list[i]+" |"+out+"\n"
                my_file.write(s)
        my_file.close()

    else:
        date_time=datetime.datetime.now()
        date_time="/appctrl/t/test/log/IPlog/"+str(date_time)+".log"
        Path(date_time).touch()
        my_file=open(date_time,"w")
        my_file.write("IP_Address |Response \n\n")
        webip_list=webnip_list
        for i in range(0,len(webip_list)):
            s2=webip_list[i]
            s1="dig www.abc.com"
            s3=".80.6."+s2+".v0.appcs.x.riverbed.cc AAAA @pastage.appcs.x.riverbed.cc +short"
            cmd=s1+s3
            proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
            out,err=proc.communicate()
            if(out==''):
                s=webip_list[i]+" |"+"No-Response"+"\n"
                my_file.write(s)
                res_flag=True
            else:
                s=webip_list[i]+" |"+out+"\n"
                my_file.write(s)  
        my_file.close()
