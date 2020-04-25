__author__ = 'Chenge'
from . import *

class Email():
    def __init__(self):
        self.db = db

    def insertemail(self,uname,receviers,title,content,head):
        '''写入新的邮件'''
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        recevers = ','.join(receviers)
        self.db.ping(reconnect=True)
        try:
            self.cur = self.db.cursor()
            self.sql = "INSERT into emaillist VALUES(DEFAULT,'{}','{}','{}','{}','{}','{}')".format(uname, recevers, title, content, nowtime,head)
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1

    def showemails(self,uname):
        '''查看所有的邮件'''
        self.list = []
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "select * from emaillist where sendname='{}'".format(uname)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        for self.i in self.res:
            self.i = list(self.i)
            self.i[2] = self.i[2].split(',')
            self.i[2] = [self.i[2][0]]+['， '+j for j in self.i[2] if self.i[2].index(j)>0]
            self.list.append(self.i)
        return self.list[::-1]

    def showEmailBin(self,id):
        '''获得删除到垃圾箱的邮件信息'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "select * from emaillist where eid={}".format(int(id))
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        return list(self.res[0])

    def deleteemail_list(self,id):
        '''删除邮件列表的邮件'''
        try:
            self.db.ping(reconnect=True)
            self.cur = self.db.cursor()
            self.sql = "delete from emaillist where eid={}".format(int(id))
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1

    def insertBinemaillist(self,List):
        '''写入垃圾箱'''
        self.db.ping(reconnect=True)
        try:
            self.cur = self.db.cursor()
            self.sql = "INSERT into emailBinlist VALUES(DEFAULT,'{}','{}','{}','{}','{}','{}')".format(List[1],List[2],List[3],List[4],List[5],List[6])
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1

    def showBin(self,uname):
        '''查询垃圾箱'''
        self.list = []
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "select * from emailBinlist where sendname='{}'".format(uname)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        for self.i in self.res:
            self.i = list(self.i)
            self.i[2] = self.i[2].split(',')
            self.i[2] = [self.i[2][0]]+['， '+j for j in self.i[2] if self.i[2].index(j)>0]
            self.list.append(self.i)
        return self.list[::-1]

    def deleteBinemail(self,id):
        '''删除垃圾箱中的邮件'''
        try:
            self.db.ping(reconnect=True)
            self.cur = self.db.cursor()
            self.sql = "delete from emailBinlist where eid={}".format(int(id))
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1

    def insertemailRough(self,uname,receviers,title,content,head):
        '''邮件写入草稿箱'''
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        recevers = ','.join(receviers)
        self.db.ping(reconnect=True)
        try:
            self.cur = self.db.cursor()
            self.sql = "INSERT into emailRough VALUES(DEFAULT,'{}','{}','{}','{}','{}','{}')".format(uname, recevers,title, content,nowtime, head)
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1

    def showRoughemail(self, uname):
        '''获取草稿箱邮件'''
        self.list = []
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "select * from emailRough where sendname='{}'".format(uname)
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        for self.i in self.res:
            self.i = list(self.i)
            self.i[2] = self.i[2].split(',')
            self.i[2] = [self.i[2][0]] + ['， ' + j for j in self.i[2] if self.i[2].index(j) > 0]
            self.list.append(self.i)
        return self.list[::-1]

    def deleteRough(self,id):
        '''删除草稿箱中的邮件'''
        try:
            self.db.ping(reconnect=True)
            self.cur = self.db.cursor()
            self.sql = "delete from emailRough where eid={}".format(int(id))
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1

    def resetRoughemail(self,id):
        '''重写某一条草稿箱邮件'''
        self.db.ping(reconnect=True)
        self.cur = self.db.cursor()
        self.sql = "select * from emailRough where eid='{}'".format(int(id))
        self.cur.execute(self.sql)
        self.res = self.cur.fetchall()
        self.save = list(self.res[0])
        self.save[2] = self.save[2].split(',')
        return self.save

    def updateRoughemail(self,id,receviers,title,content):
        '''更新已有的草稿箱邮件'''
        try:
            self.db.ping(reconnect=True)
            nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            recevers = ','.join(receviers)
            self.cur = self.db.cursor()
            self.sql = "update emailRough set receviers='{}',title='{}',content='{}',sendtime='{}' where eid='{}'".format(recevers,title,content,nowtime,id)
            self.cur.execute(self.sql)
            self.db.commit()
            return 0
        except:
            return 1