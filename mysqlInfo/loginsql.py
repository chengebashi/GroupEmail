__author__ = 'Chenge'
from . import db

class Login():

    def __init__(self):
        self.db = db

    def checkEmail(self,email):
        '''校验邮箱是否存在，0代表存在，1代表不存在'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "SELECT * from user WHERE uemail = '{}'".format(email)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        if self.res:
            return 0
        else:
            return 1

    def checkPasswd(self,number,password):
        '''登陆,0表示登陆成功,1表示密码错误'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "select * from user where uemail='{}' and upasswd = '{}'".format(number, password)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        if self.res:
            return 0
        else:
            return 1

    def showAllinfo(self,email):
        '''搜索所有的信息'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "select * from user WHERE uemail='{}'".format(email)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        return self.res[0]


    def checkroot(self,pd):
        '''校验用户名是否存在,1代表失败，0代表成功'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "SELECT upasswd from user WHERE uname = 'root'"
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        if pd==self.res[0][0]:
            return 0
        else:
            return 1

class Register():

    def __init__(self):
        self.db = db

    def checkEmail(self,email):
        '''校验邮箱是否存在，0代表存在，1代表不存在'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "SELECT * from user WHERE uemail = '{}'".format(email)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        if self.res:
            return 0
        else:
            return 1

    def checkUname(self,uname):
        '''校验用户名是否存在,0代表存在，1代表不存在'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "SELECT * from user WHERE uname = '{}'".format(uname)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        if self.res:
            return 0
        else:
            return 1

    def registerUser(self,uname,password,email):
        '注册用户，0代表成功，1代表失败'
        self.db.ping(reconnect=True)
        try:
            self.cur = self.db.cursor()
            self.sql = "INSERT into user VALUES(DEFAULT,DEFAULT,'{}','{}','{}')".format(uname,password,email)
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1




class Reset():

    def __init__(self):
        self.db = db

    def checkUname(self,uname):
        '''校验用户名是否存在,1代表存在，0代表不存在'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "SELECT * from user WHERE uname = '{}'".format(uname)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        if self.res:
            return 1
        else:
            return 0

    def resetpasswd(self,uname):
        '重置密码,0代表成功,1失败'
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        try:
            self.sql = "update user set upasswd = '123456' where uname = '{}'".format(uname)
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1

    def showemail(self,uname):
        '''查找邮箱'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "SELECT uemail from user WHERE uname='{}'".format(uname)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        return self.res[0][0]

    def updatePssword(self,uname,password):
        '''修改密码0代表成功，2代表后台错误'''
        self.db.ping(reconnect=True)
        try:
            self.cur = self.db.cursor()
            self.sql = "update user set upasswd='{}' WHERE uname='{}'".format(password, uname)
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 2

    def updateemail(self,uname,email):
        '''修改邮箱0代表成功2代表失败'''
        self.db.ping(reconnect=True)
        try:
            self.cur = self.db.cursor()
            self.sql = "update user set uemail='{}' WHERE uname='{}'".format(email, uname)
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 2

    def showuid(self,uname):
        '''查询uid'''
        db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "select uid from user WHERE uname='{}'".format(uname)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        return self.res[0][0]

    def updateheadimg(self,uid,head):
        '''写入头像,0成功,1失败'''
        db.ping(reconnect=True)
        self.cur = self.db.cursor()
        try:
            self.sql = "update user set uhead = '{}' where uid= '{}'".format(head,uid)
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1