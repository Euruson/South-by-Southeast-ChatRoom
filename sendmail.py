#! /usr/bin/env python  
# -*- coding: UTF-8 -*-  
import smtplib  
import urllib2
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
mailto_list=['497425817@qq.com']           #收件人(列表)  
mail_host="smtp.163.com"            #使用的邮箱的smtp服务器地址，这里是163的smtp地址  
mail_user="salta_salta"                           #用户名  
mail_pass="neverorforever1"                             #密码  
mail_postfix="163.com"                     #邮箱的后缀，网易就是163.com  

def SendMail(to_list,sub,content):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list                #将收件人列表以‘；’分隔
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                            #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


if __name__=="__main__":
#发送1封，上面的列表是几个人，这个就填几  
    if SendImage("497425817@qq.com","Inform","这是一个测试。"):  #邮件主题和邮件内容  
        print "done!"  
    else:  
        print "failed!"  
