# -*- coding: utf-8 -*-
__author__ = 'Administrator'
#jk409 update 2015-5-23
#import pymysql
import pymongo
#import sqlite3
#import redis
class Mysql:
    def __init__(self,host,user,password,db):
        self.cnn = pymysql.connect(host=host,user=user, passwd=password, db=db, charset='utf8')
        self.cur= self.cnn.cursor()

    def run(self,sql):
        self.cur.execute(sql)

    def cmd(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def commit(self):
        self.cnn.commit()

    def close(self):
        self.cur.close()
        self.cnn.close()

class Mongodb:
    def __init__(self, ip, port, db):
        #self.conn = pymongo.Connection(ip, port)
        self.conn = pymongo.MongoClient(ip,port)
        self.db = self.conn[db]

    def find(self,table):
        return self.db[table].find({}).limit(1500)

    def find_one(self,table,xarg):
        return self.db[table].find_one(xarg)

    def insert(self,table, xarg):
        try:
            data = self.db[table]
            data.insert(xarg)
        finally:
            self.conn.close()

    def remove(self,table ,xarg):
        try:
            data = self.db[table]
            data.remove(xarg)
        finally:
            self.conn.close()

    def save(self,table, xarg):
        try:
            data = self.db[table]
            data.save(xarg)
        finally:
            self.conn.close()

    def update(self,table ,*xarg):
        try:
            data = self.db[table]
            #data.update({"name":{'$eq':'kkk'}}, {'$set':{'age':10}}, upsert=False, multi=True)
            data.update(*xarg)
        finally:
            self.conn.close()


class Mongodb_new():
    def __init__(self, ip, port, db):
        db=self.conn = pymongo.MongoClient().test
        db.kkk.inset({'name':'kkk','age':89})





class Redis():
    def __init__(self,host,port,db,passwd):
        #AUTH password #设置redis密码
        #self.cnn=redis.Connection(host='localhost',port=6379,db=0,password='',encoding='utf-8',)
        self.cnn=redis.Redis(host=host,port=port,db=db,password=passwd,encoding='utf-8')

    def get(self,key):
        return self.cnn.get(key)

    def append(self,key,value):
        data = self.cnn
        data.append(key,value)

    def set(self,key,value):
        self.cnn.set(key,value)

    def getset(self,key,value):
        return self.cnn.getset(key,value)

    def delete(self,key):
        return self.cnn.delete(key)

    def close(self):
        pass

class Sqlite3():
    def __init__(self,db):
        self.cnn = sqlite3.connect(database=db)
        self.cur = self.cnn.cursor()

    def run(self,args):
        self.cur.execute(args)

    def cmd(self,args):
        return self.cur.execute(args)

    def commit(self):
        self.cnn.commit()

    def close(self):
        self.cnn.close()

    def INIT(self):
        sql = '''create table blog(
            id int,
            name varchar(32),
            email varchar(32),
            title varchar(32),
            fl varchar(32),
            tag varchar(32),
            date varchar(32),
            content varchar
        ) '''
        #sql2='alter table blog add column content  varchar;'
        self.cmd(sql)

if __name__ == '__main__':
    import time
    #mysql=Mysql('127.0.0.1','root','123456','blog')
    rediss=Redis('127.0.0.1',6379,0, None)
    a1=time.time()
    for i in range(1,1000000):
        rediss.set('name'+str(i),i)
    b1=time.time()
    print(a1,b1,b1-a1)
    #    sql = "insert into user (name,email,address) values ('user%s' , 'kkk@kk.com', '广东、深圳、宝安区、%s区')"%(str(i),str(i))
    #    mysql.cmd(sql)
    #mysql.commit()

    #mysql.commit()

