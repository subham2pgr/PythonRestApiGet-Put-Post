#Parsing  the domain/hostname and IP address of application from app.json
import os
import json
web_list = []
webip_list1=[]
webip_list=[]
appid=[]
websites=json.loads(open('/appctrl/navl_apps/apps.json').read())

def validIP(address):
  parts = address.split(".")
  if len(parts) != 4:
    return False
  for i in range(0,len(parts)):
    if parts[i]=='':
      return False
    if int(parts[i])<0 and int(parts[i])>255:
      return False
  return True


for i in range(0,len(websites)):
  if websites[i]["Hostname"]:
    s=websites[i]["Hostname"]
    s=s.split(' ')
    for j in range(0,len(s)):
      if s[j]:
        web_list.append(s[j])

  if websites[i]["IP/Net"]:
    ip=websites[i]["IP/Net"]
    ip=ip.split(' ')
    for j in range(0,len(ip)):
      if ip[j]:
        webip_list1.append(ip[j])
  
  if websites[i]["AppID"]:
      appid.append(websites[i]["AppID"])

for i in range(0,len(web_list)):
  web_list[i]=web_list[i].encode('ascii')
  web_list[i]=web_list[i].strip("www.")


for i in range(0,len(webip_list1)):
  webip_list1[i]=webip_list1[i].encode('ascii')
  webip_list1[i]=webip_list1[i][:-3]
  if validIP(webip_list1[i]):
    webip_list.append(webip_list1[i])

webip_list.sort()
web_list.sort()
