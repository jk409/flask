#
import sys
sys.path.append('./mymd')
from flask import Flask,jsonify,request,render_template,url_for,redirect,session,abort,escape
import time,datetime,os,copy
from mymd import sql,pgo,login_auth
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
SECRET_KEY = '123456'
app = Flask(__name__)
app.config.from_envvar('FLASKR_SETTING',silent=True)
app.secret_key = '123456'
#-----------------------------------------------------
mongo= sql.Mongodb('127.0.0.1',27017,'kkk')
#-----------------------------------------------------
@app.route('/')
def index():
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
    if login_auth.user(username):
        return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))
#-----------------------Host-------------------------------------#
@app.route('/host',methods=['GET','POST'])
def host_info():
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
    if login_auth.user(username):
        if request.method == 'POST':
            rf=request.form
            dict_host={'ip':rf['ip'],'port':rf['port'],'passwd':rf['passwd'],'group':rf['group']}            
            if rf['cmd'] == 'add':
                if login_auth.yz('host','ip',rf['ip']):
                    return redirect(url_for('host_info'))
                mongo.save('host',dict_host)
            if rf['cmd'] == 'update':
                ids = {"_id": ObjectId(rf['_id'])}
                dicts={'$set':dict_host}
                mongo.update('host',ids,dicts)
                print(time.strftime("%Y-%m-%d_%H:%M:%S"),'update_host:',rf['_id'],dict_host)
            if rf['cmd'] == 'delete':
                ids = {"_id": ObjectId(rf['_id'])}
                mongo.remove('host',ids)
                print(time.strftime("%Y-%m-%d_%H:%M:%S"),'remove_host:',rf['_id'],dict_host)    
        dbs=mongo.find('host')
        return render_template('host.html',host_active="active",data=dbs,username=username)
    else:
        return redirect(url_for('login'))
        
        
        
@app.route('/host/host_add',methods=['GET','POST'])
def host_add():
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']            
    if login_auth.user(username):
        if request.method == 'POST':
            rf=request.form
            if login_auth.yz('host','ip',rf['ip']):         
                return render_template('host_add.html',host_active="active",username=username,host_add_fail=rf['ip'])               
            dict_ip={'ip':rf['ip'],'port':rf['port'],'passwd':rf['passwd'],'group':rf['group']}
            mongo.insert('host',dict_ip)
            print(time.strftime("%Y-%m-%d_%H:%M:%S"),'add:',dict_ip)
            return render_template('host_add.html',host_active="active",username=username,host_add_ok=rf['ip'])  
        return render_template('host_add.html',host_active="active",username=username)    
    else:
        return redirect(url_for('login'))

@app.route('/host/host_mod/<id>',methods=['GET','POST'])
def host_mod(id):
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
        ids = {"_id": ObjectId(id)}             
    if login_auth.user(username):
        if request.method == 'POST':
            rf=request.form
            dict_host={'ip':rf['ip'],'port':rf['port'],'passwd':rf['passwd'],'group':rf['group']}
            mongo.update('host',ids, {'$set':dict_host})      
        mongo.find_one('host',ids)
        print(dbs)
        return render_template('host_mod.html',user_active="active",username=username,data=dbs)
    else:
        return redirect(url_for('login'))


        
        
@app.route('/host/host_del/<id>')
def host_del(id):
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
    if login_auth.user(username):
        ids = {"_id": ObjectId(id)}
        mongo.remove('host',ids)
        print(time.strftime("%Y-%m-%d_%H:%M:%S"),'delete:',id,ids)
        return redirect(url_for('host'))
    else:
        return redirect(url_for('login'))
#----------------------end Host---------------------------------#  
      
@app.route('/user',methods=['GET','POST'])
def user():
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
  
    if login_auth.user(username):
        if request.method == 'POST':
            rf=request.form
            if rf['cmd'] == 'add_user':
                dict_user={'name':rf['name'],'passwd':rf['passwd'],'age':rf['age'],'bm':rf['bm'],'date':(time.strftime("%Y-%m-%d_%H:%M")),'mod_date': (time.strftime("%Y-%m-%d_%H:%M"))}
                print('--------------------------------',dict_user)
                mongo.save('users',dict_user)
                return redirect(url_for('user'))
            if rf['cmd'] == 'add_group':
                dict_group={'user_group':rf['new_group']}
                mongo.save('groups',dict_group)
            if rf['cmd'] == 'del_group':
                dict_group={'user_group':rf['new_group']}
                mongo.remove('groups',dict_group)
    dbs=mongo.find('users')
    gps=mongo.find('groups')
    return render_template('index.html',user_active="active",data=dbs,gps=gps,username=username)

        
@app.route('/mod_user/<id>',methods=['GET','POST'])
def mod_user(id):
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
        ids = {"_id": ObjectId(id)}             
    if login_auth.user(username):
        if request.method == 'POST':
            rf=request.form
            dict_user={'name':rf['name'],'passwd':rf['passwd'],'age':rf['age'],'bm':rf['bm'],'date':rf['date'],'mod_date': (time.strftime("%Y-%m-%d_%H:%M"))}
            add_user={'name':rf['name'],'passwd':rf['passwd'],'age':rf['age'],'bm':rf['bm'],'date':(time.strftime("%Y-%m-%d_%H:%M")),'mod_date': (time.strftime("%Y-%m-%d_%H:%M"))}
            if rf['cmd'] == 'update':
                mongo.update('users',ids, {'$set':dict_user})
                print(time.strftime("%Y-%m-%d %H:%M:%S"),'update:',id,dict_user)
            if rf['cmd'] == 'add':        
                mongo.save('users',add_user)
        dbs=mongo.find_one('users',ids)
        print(dbs,'\n',dbs['name'])
        return render_template('mod_user.html',user_active="active",username=username,data=dbs)
    else:
        return redirect(url_for('login'))

@app.route('/delete/<id>',methods=['GET','POST'])
def delete(id):
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
    if login_auth.user(username):
        ids = {"_id": ObjectId(id)}
        mongo.remove('users',ids)
        print(time.strftime("%Y-%m-%d_%H:%M:%S"),'delete:',id,ids)
        return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))
            
    
@app.route('/info')
def info():
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
        dbs = pgo.pgo('127.0.0.1',27017,'kkk','view').run()
        #db_list = []
        #for db in dbs:
        #    db_list.append(db)
        return render_template('info.html',info_active="active",username=username,data=dbs)
 

 
@app.route('/ll')
def ll():
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password'] 
        return render_template('ll.html',ll_active="active",username=username)

        
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file_list = []
    UPLOAD_DIR="static/upload/"
    if 'username' not in session or session['username'] == '':
        return redirect(url_for('login'))
    else:
        username = session['username']
        passwd = session['password']
    file = os.popen("ls %s"%UPLOAD_DIR)
    for i in file:
        file_path = UPLOAD_DIR+str(i.split()[0])
        s = os.path.getmtime(file_path)
        tt=time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime( float(s)))
        file_list.append([i,os.path.getsize(file_path),tt])
        
    if request.method == 'POST':        
        if request.form['cmd'] == 'upload':
            f = request.files['file']
            fname = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_DIR,fname))
            return render_template('upload.html',username=username,file_active="active",file=fname,file_list=file_list)    

        if request.form['cmd']:
            file = UPLOAD_DIR+request.form['cmd']
            if os.path.isfile(file):
                os.remove(file)
    return render_template('upload.html',username=username,file_active="active",file_list=file_list)
        


    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['email']
        session['password'] = request.form['password']
        username = session['username']
        passwd = request.form['password']
        print(username,passwd)
        return redirect(url_for('user'))
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('username',None)
    session.pop('passwd',None)
    return redirect(url_for('login'))
    
      
    
if __name__ == '__main__':
    #app.run()
    #host IP
    #port 端口
    #threaded  多线程
    #debug  调试
    app.run(host='0.0.0.0',port=8080,debug=True)
