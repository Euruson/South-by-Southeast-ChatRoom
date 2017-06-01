 # -*- coding:utf-8 -*-
import os
import sys
import json
import time
import tornado.httpserver
import tornado.web
import tornado.ioloop
import md5
import thread
from tornado import websocket
import random
import uuid
import sendmail
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

themeColor=['red','blue','green','black','gray','yellow']
count=0
listenPort=80
#address="www.shadowwalker.cn"
address="127.0.0.1"
sessions={}
log=open("log.txt","a")

def getTime():
    return '['+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'] '

class Index(tornado.web.RequestHandler):
    def get(self):
        global listenPort
        if(self.get_secure_cookie('status')!='logined'):
            self.redirect('login.html')
            return
        if not self.get_secure_cookie('uid'):
            setUid="1234"
            self.set_secure_cookie('uid',setUid)
        self.render('chatTemplate.html',lp=listenPort,ipAddress=address)
class VerifyHandler(tornado.web.RequestHandler):
    def get(self):
        action=self.get_argument('action')
        print '[verify]',action
        sql=sqlite3.connect("chatroom.db")
        cur=sql.execute("select name from user where verify='{}'".format(action))
        res=cur.fetchall()
        if(len(res)!=0):#使能账户
            sql.execute("update user set valid=1 where verify='{}'".format(action))
        else:
            print "[-]Wrong check"
        self.render('login.html')
        sql.commit()
        sql.close()


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_secure_cookie('uid'):
            setUid="1234"
            self.set_secure_cookie('uid',setUid)
        self.render('login.html')
    def post(self):
        username=self.get_argument('txtName')
        password=self.get_argument('txtPwd')
        sql=sqlite3.connect("chatroom.db")
        cur=sql.execute("select id from user where name='{}' and password='{}' and valid=1".format(username,password))
        res=cur.fetchall()
        if(len(res)!=0):#密码匹配
            self.set_secure_cookie('status','logined')
            self.redirect("/")
        else:
            cur=sql.execute("select id from user where name='{}' and password='{}' and valid=0".format(username,password))
            res=cur.fetchall()
            self.set_secure_cookie('status','notLogin')
            if(len(res)!=0):
                self.redirect('login.html?error=0')
            else:
                self.redirect('login.html?error=1')

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')
    def post(self):
        username=self.get_argument('txtName')
        password=self.get_argument('txtPwd')
        sex=self.get_argument('sex')
        txtEmail=self.get_argument('txtEmail')
        txtColege=self.get_argument('txtColege')
        print "[Regist]",username,password,sex,txtEmail,txtColege
        sql=sqlite3.connect("chatroom.db")
        sql.execute("insert into user (name,password,email,gender,verify,valid) values('{}','{}','{}','{}','{}','{}')".format(username,password,txtEmail,sex,md5.md5(username).hexdigest(),0))
        sql.commit()
        sql.close()
        varifyUrl="http://"+address+"/verify?action="+md5.md5(username).hexdigest()
        mailword='{}，您好，感谢您的注册，请点击下方的注册确认链接完成注册。\n{}'.format(username,varifyUrl)
        sendmail.SendMail(txtEmail,"[东南偏南聊天室]请确认您的注册信息",mailword)
        self.redirect('/login.html')

def combineInfo(message_="[]",toWho_="everyone",id_=0,userName_="Annormous",status_="chat",color_="black"):
        strJ="{message:'"+message_+"',toWho:'"+toWho_+"',id:"+str(id_)+",userName:'"+userName_+"',status:'"+status_+"',color:'"+color_+"'}"
        return strJ

class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    global themeColor
    global sessions


    @staticmethod
    def repeat_user_name(username):
        for u in SocketHandler.clients:
            if u.my_user_name==username:
                return True
        return False

    @staticmethod
    def send_to_all(message):
        for c in SocketHandler.clients:
            c.write_message(message)

    @staticmethod
    def update_member(ss):
        clientInfo="{"
        for c in SocketHandler.clients:
            clientInfo=clientInfo+c.my_user_name+":"+"1,"
        clientInfo=clientInfo+"}"
        if(clientInfo[-2]==','):
            clientInfo=clientInfo[:-2]+"}"
        dataToSend=combineInfo(message_=clientInfo,status_='updateMember')
        print "[+]updateMemeber self"
        ss.write_message(dataToSend)

    @staticmethod
    def update_member_to_all():
        clientInfo="{"
        for c in SocketHandler.clients:
            clientInfo=clientInfo+c.my_user_name+":"+"1,"
        clientInfo=clientInfo+"}"
        if(clientInfo[-2]==','):
            clientInfo=clientInfo[:-2]+"}"
        dataToSend=combineInfo(message_=clientInfo,status_='updateMember')
        print "[+]updateMemeber all"
        SocketHandler.send_to_all(dataToSend)

    def open(self):
        self.my_color_name="black"
        self.my_user_name='Anonymous'+str(id(self))[-6:]
        print str(id(self)) + ' has joined'
        logStr=getTime()+self.my_user_name+' joined\n'
        log.write(logStr)
        log.flush()	
        self.my_color_name=themeColor[int(random.random()*6)]
        print 'Color:',self.my_color_name
        dataToSend=combineInfo(id_=id(self),userName_=self.my_user_name,status_='varify',color_=self.my_color_name)
        self.write_message(dataToSend)
        SocketHandler.clients.add(self)
        dataToSend=combineInfo(userName_=self.my_user_name,status_='join')
        print "[+]join all"
        SocketHandler.send_to_all(dataToSend)
        SocketHandler.update_member(self)


    def on_close(self):
        SocketHandler.clients.remove(self)
        dataToSend=combineInfo(userName_=self.my_user_name,status_='remove')
        print "[+]remove all"
        SocketHandler.send_to_all(dataToSend)
        print str(id(self)) + ' has left'
        logStr=getTime()+self.my_user_name+' left\n'

    def on_message(self, message):
        message = json.loads(message)
        print 'on_message:',message
        if(message['status']=='chat'):
            tmp=message['message']
            logStr=getTime()+self.my_user_name+': '+tmp+'\n'
            log.write(logStr)
            log.flush()
            tmp=tmp.replace('\n','<br>')
            tmp=tmp.replace('<script>','$hack')
            tmp=tmp.replace('</script>','$hack')
            message['message']=tmp
            print "replace ",tmp
            dataToSend=combineInfo(userName_=message['userName'],id_=message['id'],message_=message['message'],toWho_="everyone",status_="chat",color_=message['color'])
            SocketHandler.send_to_all(dataToSend)
        elif(message['status']=='userNameChange'):
            tmpSession={'userName':message['userName'],'id':str(id(self)),'color':self.my_color_name}
            tmpUid=self.get_secure_cookie('uid')
            sessions[tmpUid]=tmpSession
            logStr=getTime()+self.my_user_name+' try to change nick name to '+message['userName']+'\n'
            log.write(logStr)
            log.flush()
            if(SocketHandler.repeat_user_name(message['userName'])):
                dataToSend=combineInfo(message_="repeat",id_=id(self),userName_=self.my_user_name,status_='varify',color_=self.my_color_name)
                print "[+]repeat self"
                self.write_message(dataToSend)
            else:
                dataToSend=combineInfo(id_=id(self),userName_=message['userName'],status_='varify',color_=self.my_color_name)
                self.write_message(dataToSend)
                self.my_user_name=message['userName']
                print "[+]updateName all"
                SocketHandler.update_member_to_all()
        elif(message['status']=='updateMember'):
            print "query for update member"
            SocketHandler.update_member(self)

        #print sessions

def checkTast():
    time.sleep(1)
    count=0
    while True:
        count=count+1
        print "System beep "+str(count)
        SocketHandler.send_to_all("{'stamp':"+str(count)+"}")
        time.sleep(10)

if __name__ == '__main__':
    app = tornado.web.Application([
        ('/', Index),
        ('/soc', SocketHandler),
        ('/login.html',LoginHandler),
        ('/login.action',LoginHandler),
        ('/register.html',RegisterHandler),
        ('/verify',VerifyHandler)
    ],cookie_secret='abcd',
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    print "Running"
    thread.start_new_thread(checkTast,())
    app.listen(listenPort)
    tornado.ioloop.IOLoop.instance().start()
