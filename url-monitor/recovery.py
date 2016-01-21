#!/usr/bin/python
#coding=utf-8

from urllib2 import Request, urlopen, URLError
import urllib2
import sys
import json
import time
import smtplib
from email import encoders
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.text import MIMEText
reload(sys) 
sys.setdefaultencoding( "utf-8" )


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr.encode('utf-8') if isinstance(addr,unicode) else addr))

def SendMail(subject,content):
    from_addr = "From_Email@163.com"
    password = "From_Email_password"
    to_addr = "Dest_Email@qq.com"
    smtp_server = "smtp.163.com"

    msg = MIMEText('%s' % content,"plain","utf-8") 
    msg['From'] = _format_addr(u'MPP-monitor <%s>' % from_addr)
    msg['To'] = _format_addr(u'MPP-OPS <%s>' % to_addr)
    msg['Subject'] = Header(u'%s' % subject).encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(0)
    server.login(from_addr, password)
    server.sendmail(from_addr,[to_addr],msg.as_string())
    server.quit()

def writeLog(info,file):
    with open(file,'a') as logFile:
        logFile.write(info)
        logFile.write('\n')

#将恢复的接口和主机从error文件中删除
def delete_msg(file_url,host,url):
    with open(file_url,'r') as errorFile:
        error_msg_dict = json.load(errorFile)
        error_msg_dict.get(host).remove(url)
        if len(error_msg_dict.get(host)) == 0:
            error_msg_dict.pop(host)
    with open(file_url,'w') as errorFile:
        error_msg_json = json.dumps(error_msg_dict,sort_keys=True,indent=2)
        errorFile.write(error_msg_json)

#判断请求的url和host是否在error文件里面
def filter_msg(file_url,host,url):
    with open(file_url,'r') as errorFile:
        error_msg_dict = json.load(errorFile)
        if error_msg_dict.has_key(host) and url in error_msg_dict.get(host):
            return True
        else:
            return False

#重试
def try_again(errorFile,host,url):
    req = urllib2.Request(url)
    req.set_proxy('%s:80'%host,'http')
    try:
        r = urllib2.urlopen(req)
    except URLError, e:
        if hasattr(e,'reason'):
	    info = "%s | AWS-monitor \n 报错主机：%s \n 报错接口：%s \n 错误详情： %s" % (Now,host,url,e)
        elif hasattr(e,'code'):
	    info = "%s | AWS-monitor \n 报错主机：%s \n 报错接口：%s \n 错误详情： %s" % (Now,host,url,e)
    else:
        resp = json.loads(r.read())
        if "err_code" in resp and resp['err_code'] != 200:
            info = "%s | AWS-monitor \n 报错主机：%s \n 报错接口：%s \n 错误代码： %s \n 错误详情：%s" % (Now,host,url,resp['err_code'],resp['err_msg'])
        elif "code" in resp and resp['code'] != 200:
            info = "%s | AWS-monitor \n 报错主机：%s \n 报错接口：%s \n 错误代码： %s \n 错误详情：%s" % (Now,host,url,resp['err_code'],resp['err_msg'])
        else:
            info = "%s | AWS-monitor \n 请求主机：%s \n 请求接口：%s \n 状态码： %s " % (Now,host,url,resp['err_code'])
            delete_msg(error_file,host,url)
            SendMail("MPP-url-recovery",info)
    writeLog(info,LogFile)


HostFile = "./host.json"
UrlFile = "./url.json"
error_file = "./error.json"
LogFile = "./monitor.log"
Now = time.strftime('%Y-%m-%d %H:%M:%S')

with open(error_file,'r') as errorFile:
    error_msg_dict = json.load(errorFile)
    for host in error_msg_dict.keys():
        for url in error_msg_dict.get(host):
 	    req = urllib2.Request(url)
	    req.set_proxy('%s:80'%host,'http')
	    try:
	        r = urllib2.urlopen(req,timeout=2)
	    except URLError, e:
	        if hasattr(e,'reason'):
	            try_again(error_file,host,url)
	        elif hasattr(e,'code'):
		    try_again(error_file,host,url)
	    else:
		resp = json.loads(r.read())
                if "err_code" in resp and resp['err_code'] != 200:
		    try_again(error_file,host,url)
                elif "code" in resp and resp['code'] != 200:
		    try_again(error_file,host,url)
   		else:
		    try_again(error_file,host,url)
