__author__ = 'Administrator'
#pip install  pymongo
#from bson.objectid import ObjectId
import pymongo
import  time

class pgo:
    def __init__(self, ip, port, db, tb):
        self.ip = ip
        self.port = port
        self.db = db
        self.tb = tb
        self.conn = pymongo.MongoClient(ip,port)

    def run(self):
        try:
            db = self.conn[self.db]
            data = db[self.tb].find({}).limit(1500)
            return data
        except Exception as e:
            self.conn.close()

    def find(self,xarg):
        try:
            db = self.conn[self.db]
            data = db[self.tb].find_one(xarg)
            return data
        except Exception as e:
            self.conn.close()

    def add(self, xarg):
        try:
            db = self.conn[self.db]
            data = db[self.tb]
            data.insert(xarg)
            self.conn.close()
        except:
            self.conn.close()

    def remove(self, xarg):
        try:
            db = self.conn[self.db]
            data = db[self.tb]
            data.remove(xarg)
            self.conn.close()
        except:
            self.conn.close()

    def insert(self, xarg):
        try:
            db = self.conn[self.db]
            data = db[self.tb]
            data.insert(xarg)
            self.conn.close()
        except:
            self.conn.close()

    def save(self, xarg):
        try:
            db = self.conn[self.db]
            data = db[self.tb]
            data.save(xarg)
            self.conn.close()
        except:
            self.conn.close()

    def update(self, *xarg):
        try:
            db = self.conn[self.db]
            data = db[self.tb]
            #data.update({"name":{'$eq':'kkk'}}, {'$set':{'age':10}}, upsert=False, multi=True)
            data.update(*xarg, upser=False, multi=True)
            self.conn.close()
        except:
            self.conn.close()



if  __name__ == '__main__':
    #pgo('127.0.0.1', 27017, 'kkk', 'kkk').remove({'name':'kkk', 'age':{"$gte":32}})
    #pgo('127.0.0.1', 27017, 'kkk', 'kkk').add('kkk', 99, 'OP')
    #pgo('127.0.0.1', 27017, 'kkk', 'kkk').update({}, {'$set':{'date': (time.strftime("%Y-%m-%d_%H:%M")), 'mod_date': (time.strftime("%Y-%m-%d_%H:%M"))}})
    pgo('127.0.0.1', 27017, 'kkk', 'kkk').run()



