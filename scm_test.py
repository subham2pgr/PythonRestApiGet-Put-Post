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

scm_flag = False

#Function to get the latest pattern file downloaded by scm and performing sanity test,get all pattern deployed list, get healthcheck, get scm patern latest version and getall pattern file in dynamodb
def scm_test():
	mydir = os.path.join(
        '/appctrl/t/test/log/scm_tgz_file', 
        datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
	os.mkdir(mydir)
	date_time=datetime.datetime.now()
	date_time="/appctrl/t/test/log/Patternlog/"+str(date_time)+".log"
	Path(date_time).touch()
	my_file=open(date_time,"w")
	pattern_deployed='curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/patterns'
	getproc=subprocess.Popen(shlex.split(pattern_deployed),stdout=subprocess.PIPE)
	pattern_deployedout,pattern_derr=getproc.communicate()
	s=pattern_deployedout+"\n"
	my_file.write("All Pattern Deployed List \n")
	my_file.write(s)
	healthcheck='curl -s https://3t56vnjb51.execute-api.ap-south-1.amazonaws.com/internal/healthcheck'
	getproc=subprocess.Popen(shlex.split(healthcheck),stdout=subprocess.PIPE)
	healthcheck_out,healthcheck_err=getproc.communicate()
	s=healthcheck_out+"\n"
	myfile_write("Healthcheck \n")
	myfile_write(s)
	pattern_resp='curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/scm_pattern_version/LATEST'
	getproc=subprocess.Popen(shlex.split(pattern_resp),stdout=subprocess.PIPE)
	pattern_out,pattern_err=getproc.communicate()
	s=pattern_out+"\n"
	my_file.write("SCM pattern latest version \n")
	my_file.write(s)
	dbcmd='curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/patterns'
	getproc=subprocess.Popen(shlex.split(dbcmd),stdout=subprocess.PIPE)
	db_out,db_err=getproc.communicate()
	s=db_out+"\n"
	my_file.write("GET all the available versions of pattern file in dynamoDB \n")
	my_file.write(s)
	my_file.close()
	url ='http://pagg-staging.riverbed.cc/api/aggregator/1.0/scm_patterns'
	filename=wget.download(url,out=mydir)
	tarfile=os.path.join(mydir,'scm_patterns')
	path=mydir
	r=subprocess.call(['tar', '-xzf', tarfile, '-C', path])
	if(r==0):
		appgrpjson_path=os.path.join(mydir,'appgroups.json')
		appgrpjson = os.path.getsize(appgrpjson_path)
		appjson_path=os.path.join(mydir,'apps.json')
		appjson = os.path.getsize(appjson_path)
		favicon_path=os.path.join(mydir,'favicon')
		favicon = os.path.getsize(favicon_path)
		webcat_path=os.path.join(mydir,'webcats.json')
		webcatjson = os.path.getsize(webcat_path)
		if appgrpjson < 1:
			scm_flag=True
		if appjson < 1:
			scm_flag=True
		if favicon < 1:
			scm_flag=True
		if webcatjson < 1:
			scm_flag=True
