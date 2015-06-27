import os,time
class kkk:
    def __init__(self,name,age,job):
        self.name = name
        self.age =  age
        self.job = job

    def run(self):
        print (self.name,'today is',self.age,'todo',self.job)

def IP(ip):
    os.system('ping %s'%ip)

if __name__ =="__main__":
    kkk('jk409',25,'IT').run()
    IP('8.8.8.8')
