#!/usr/bin/python2.7
#coding=utf-8

import sys
import json
import time
import smtplib
from email import encoders
from email.header import Header
from email.utils import parseaddr,formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
reload(sys)
sys.setdefaultencoding( "utf-8" )

'''
格式化邮件地址
'''
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr.encode('utf-8') if isinstance(addr,unicode) else addr))
'''
主函数，读取邮件发送内容和接收人并发送
'''
department = sys.argv[1]

if department == 'MPP':
    to_addr = "Dest_Email@email.com"
    html_file = './MPP.html'
elif department == 'pf':
    to_addr = "Dest_Email@email.com"
    html_file = './pf.html'
else:
    to_addr = "Dest_Email@email.com"
    html_file = './MPP.html'



from_addr = "From_Email@163.com"
password = "From_Email_passwd"
smtp_server = "smtp.163.com"
subject = "服务器周报"

msg = MIMEMultipart('alternatvie')
html = open(html_file).read()
html_part = MIMEText(html,_subtype="html",_charset="utf-8")
msg.attach(html_part)
msg['From'] = _format_addr(u'monitor <%s>' % from_addr)
msg['To'] = _format_addr(u'OPS <%s>' % to_addr)
msg['Subject'] = Header(u'%s' % subject).encode()
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(0)
server.login(from_addr, password)
server.sendmail(from_addr,[to_addr],msg.as_string())
server.quit()
