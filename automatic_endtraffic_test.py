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
import run_dig_cmd as dig_cmd
import PA_stage_test as PA
import getcmd_for_allappid as getcmd
import scm_test as scm
import geo_dns_cmd as geo
import fetch_all_app_pattern as pattern
import dyanmic_test as dyanmic_test

web_list=wb.web_list
webip_list=wb.webip_list
diff_flag=False
res_flag = False

#Function to compare the latest previous file with the current file in order to check the difference in response
def compare_file_for_diff(list_of_files):
    list_of_files.sort(key=lambda x: os.path.getmtime(x))
    latest_file1 = max(list_of_files, key=os.path.getctime)
    if len(list_of_files) > 1:
        latest_file2=list_of_files[len(list_of_files)-2]
        with open(latest_file2, 'r') as f1, open(latest_file1,'r') as f2:
            for x,y in zip(f1,f2):
                if(x!=y):
                    diff_flag=True
                    print(x,y)


#Function To delete the old file if its older than 30day

def delete_file_monthly(folder):
    now = time.time()
    files = [os.path.join(folder, filename) for filename in os.listdir(folder)]
    for filename in files:
        if (now - os.stat(filename).st_mtime) > 30*24*60*60:
            os.remove(filename)

#Function to Send the email in case if there is diff in response or ACS server not Responsing
def send_email(reply):
    msg = MIMEMultipart()
    msg['Subject'] =  ('ACS End to End Traffic Response Issue FROM ')
    msg['From'] = 'pverma@riverbed.com'
    msg['Reply-to'] = 'pverma@riverbed.com'
    msg.preamble = 'Multipart massage.\n'

    if reply==1:
        part = MIMEText("ACS SERVER is NOT Responsing")
    if reply==0:
        part = MIMEText("There is Difference Response from Previous Response")
    if reply==2:
        part= MIMEText("There is problem in downloading tgz file to scm")
    msg.attach(part)

    s = smtplib.SMTP('riverbed-com.mail.protection.outlook.com')
    emaillist = ["Eng-appctrl@riverbed.com"]
    msg['To'] = ', '.join(emaillist)
    s.sendmail(msg['From'], emaillist , msg.as_string())
    s.quit()


dig_cmd.run_cmd(web_list,"weblist")
dig_cmd.run_cmd(webip_list,"webiplist")

list_of_domainfiles = glob.glob('/appctrl/t/test/log/domainlog/*')
compare_file_for_diff(list_of_domainfiles)
list_of_IPfiles = glob.glob('/appctrl/t/test/log/IPlog/*')
compare_file_for_diff(list_of_IPfiles)

domainfolder = '/appctrl/t/test/log/domainlog'
delete_file_monthly(domainfolder)
ipfolder = '/appctrl/t/test/log/IPlog'
delete_file_monthly(ipfolder)

PA.PA_stage_test()
pafolder = '/appctrl/t/test/log/PAlog'
delete_file_monthly(pafolder)

getcmd.getcmd_frall_appid()
applogfolder = '/appctrl/t/test/log/AppIDlog'
delete_file_monthly(applogfolder)

scm.scm_test()
patternfolder = '/appctrl/t/test/log/Patternlog'
delete_file_monthly(patternfolder)

geo.geo_dns_cmd()
dnsfolder= '/appctrl/t/test/log/GeoDns'
delete_file_monthly(dnsfolder)

pattern.fetch_all_app_pattern()
app_pattern_folder='/appctrl/t/test/log/AppPattern'
delete_file_monthly(app_pattern_folder)

dyanmic_test.dyanmic_cmd()
bootstrap_folder='/appctrl/t/test/log/bootstraplog'
delete_file_monthly(bootstrap_folder)

if diff_flag:
    send_email(0)
if res_flag:
    send_email(1)
if scm.scm_flag:
    send_email(2)


