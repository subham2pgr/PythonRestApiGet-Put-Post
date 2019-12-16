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

#Function Fetch pattern definitions for all apps
def fetch_all_app_pattern():
	date_time=datetime.datetime.now()
	date_time="/appctrl/t/test/log/AppPattern/"+str(date_time)+".log"
	Path(date_time).touch()
	my_file=open(date_time,"w")
	key="\"X-API-Key: mPXWeT7Q2S9rD7Fo9gZwL8xBB0M66UMO970zQe7g\""
	cmd="curl -s -H " +key+ " https://stage-aggregator.rvbd-staging.cloudns.cc/applications"
	getproc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
	cmd_out,cmd_err=getproc.communicate()
	my_file.write(cmd_out)
	my_file.close()
