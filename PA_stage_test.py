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

app_id_dict={
        "206":"2.2.2.2",
        "1111":"2.2.2.3",
        "1143":"2.2.2.4"
}
#Function to test the PA stage PUT,POST and GET and dig cmd using changed IP
def PA_stage_test():
	date_time=datetime.datetime.now()
	date_time="/appctrl/t/test/log/PAlog/"+str(date_time)+".log"
	Path(date_time).touch()
	my_file=open(date_time,"w")
	for k,v in app_id_dict.iteritems():
		postcmd='curl -s -H "X-API-Key: mPXWeT7Q2S9rD7Fo9gZwL8xBB0M66UMO970zQe7g"  https://stage-aggregator.rvbd-staging.cloudns.cc/patterns -X POST'
		getcmd= 'curl -s https://stage-aggregator.rvbd-staging.cloudns.cc/patterns'
		api="\"X-API-Key: mPXWeT7Q2S9rD7Fo9gZwL8xBB0M66UMO970zQe7g\""
		url=" https://stage-aggregator.rvbd-staging.cloudns.cc/applications/"+k+" -H "
		content="\'Content-Type: application/json\'"
		key="\"ipv4s\""
		value="\""+v+"\""
		data="\'{"+key+": ["+value+"]}\'"
		putcmd="curl -s -H "+api+url+content+" -X PUT --data "+data
		putproc=subprocess.Popen(shlex.split(putcmd),stdout=subprocess.PIPE)
		putout,puterr=putproc.communicate()
		postproc=subprocess.Popen(shlex.split(postcmd),stdout=subprocess.PIPE)
		postout,posterr=postproc.communicate()
		getproc=subprocess.Popen(shlex.split(getcmd),stdout=subprocess.PIPE)
		getout,geterr=getproc.communicate()
		s2=v
		s1="dig www.abc.com"
		s3=".80.6."+s2+".v0.appcs.x.riverbed.cc AAAA @pastage.appcs.x.riverbed.cc +short"
		cmd=s1+s3
		proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
		out,err=proc.communicate()
		my_file.write("PA stage testing for app_id"+str(k)+"\n")
		my_file.write("PUT\n")
		s=putout+"\n"
		my_file.write(s)
		my_file.write("Deploy\n")
		s=postout+"\n"
		my_file.write(s)
		my_file.write("get patteren\n")
		s=getout+"\n"
		my_file.write(s)
		my_file.write("end_to_end\n")
		s=out+"\n"
		my_file.write(s)
        my_file.close()

