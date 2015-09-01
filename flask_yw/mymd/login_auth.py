__author__ = 'Administrator'
from mymd import pgo
#import hashlib
#a="1234"
#hashlib.md5(a.encode('utf-8')).hexdigest()
def user(username):
    na = pgo.pgo('127.0.0.1',27017,'kkk','user').find({"name": username})
    if na:
        return True
    else:
        return False

def add_user(username):
    na = pgo.pgo('127.0.0.1',27017,'kkk','user').find({"name": username})
    if na:
        return True
    else:
        return False
def yz(db,table, zd, username):
    na = pgo.pgo('127.0.0.1', 27017, db, table).find({zd: username})
    if na or username == '':
        return True
    else:
        return False

if  __name__ == '__main__':
    user('kkk')
