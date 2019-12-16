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

#Function Validate the dynamic update behaviour of Pattern aggregator
def dyanmic_cmd():
	#This test case checks for bootstrapping support during boot up of aggregator.
	#GET patternns
	date_time=datetime.datetime.now()
	date_time="/appctrl/t/test/log/bootstraplog/"+str(date_time)+".log"
	Path(date_time).touch()
	my_file=open(date_time,"w")
	pattern_cmd='curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/patterns'
	getproc=subprocess.Popen(shlex.split(pattern_cmd),stdout=subprocess.PIPE)
	pattern_cmd_out,pattern_cmd_err=getproc.communicate()
	my_file.write("GET Pattern \n")
	s=pattern_cmd_out+"\n"
	my_file.write(s)
	#Verify if pattern file version gets revised after update for each deployment.
	get_cmd='curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/scm_pattern_version/LATEST'
	getproc=subprocess.Popen(shlex.split(get_cmd),stdout=subprocess.PIPE)
	get_cmd_out,get_cmd_err=getproc.communicate()
	my_file.write("GET the latest pattern file version \n")
	s=get_cmd_out+"\n"
	my_file.write(s)
	my_file.write("Update app information \n")
	key="\"X-API-Key: mPXWeT7Q2S9rD7Fo9gZwL8xBB0M66UMO970zQe7g\""
	url=" https://stage-aggregator.rvbd-staging.cloudns.cc/applications/206 -H "
	content="\'Content-Type: application/json\'" + " -X PUT --data "
	item="\"app_desc\"" +": "+ "\"Facebook\""
	data="\'{"+item+"}\'"
	put_cmd="curl -s -H " +key+ url+ content+ data
	getproc=subprocess.Popen(shlex.split(put_cmd),stdout=subprocess.PIPE)
	put_cmd_out,put_cmd_err=getproc.communicate()
	s=put_cmd_out+"\n"
	my_file.write(s)
	#POST the changes
	post_cmd="curl -s -H "+key+" https://stage-aggregator.rvbd-staging.cloudns.cc/scm_patterns -X POST"
	getproc=subprocess.Popen(shlex.split(post_cmd),stdout=subprocess.PIPE)
	post_cmd_out,post_cmd_err=getproc.communicate()
	my_file.write("POST the changes \n")
	s=post_cmd_out+"\n"
	my_file.write(s)
	#GET the latest pattern file version
	get_cmd='curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/scm_pattern_version/LATEST'
	getproc=subprocess.Popen(shlex.split(get_cmd),stdout=subprocess.PIPE)
	get_cmd_out,get_cmd_err=getproc.communicate()
	my_file.write("GET the latest pattern file version \n")
	s=get_cmd_out+"\n"
	my_file.write(s)
	for app_id in appid:
		cmd='curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/applications/'+str(app_id)
		getproc=subprocess.Popen(shlex.split(pattern_cmd),stdout=subprocess.PIPE)
		cmd_out,cmd_err=getproc.communicate()
		s=cmd_out+"\n"
		my_file.write("GET application info dump for app_id"+str(app_id)+"\n")
		my_file.write(s)

	my_file.close()
