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

appid=wb.appid
#Function to run the get and dig command for all appid present in the apps.json file
def getcmd_frall_appid():
    date_time=datetime.datetime.now()
    date_time="/appctrl/t/test/log/AppIDlog/"+str(date_time)+".log"
    Path(date_time).touch()
    my_file=open(date_time,"w")
    for id in appid:
        getcmd='curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/applications/'+str(id)
        getproc=subprocess.Popen(shlex.split(getcmd),stdout=subprocess.PIPE)
        getout,geterr=getproc.communicate()
        dic=yaml.load(str(getout))
        if dic["hostnames"]:
            host=dic["hostnames"][0].strip(".")
            s2="www."+host
            s1="dig "
            s3=".80.6.1.2.3.4.v0.appcs.x.riverbed.cc AAAA @pastage.appcs.x.riverbed.cc +short"
            cmd=s1+s2+s3
            proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
            out,err=proc.communicate()
            s=str(id)+" "+str(host)+"\n"
            my_file.write(s)
            s=getout+"\n"
            my_file.write(s)
            s=out+"\n"
            my_file.write(s)
    my_file.close()
