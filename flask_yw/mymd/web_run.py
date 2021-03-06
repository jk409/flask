#coding=utf-8
__author__ = 'Administrator'
import time,sqlite3,random
#import tornado.autoreload
#import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.template
import tornado.httpclient
import tornado.gen

from tornado.options import define, options
define("port", default=80, help="run on the given port", type=int)
page = 0
class sql:
    def __init__(self):
        self.cnn = sqlite3.connect(database='blog.db')
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

#实例化sql类
sql = sql()

class myapp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/test", BlogsHandler),
            (r"/test/([0-9]+)", BlogshowHandler),
            (r"/test/add", BlogaddHandler),
            (r"/test/edit/([0-9]+)", BlogeditHandler),
            (r"/test/(.*)", BlogsflHandler),
            (r"/xml", XmlHandler),
            (r"/uedit", sqlHandler),
            (r"/upload", uploadHandler),
        ]
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            'template_path':'templates',
            'static_path' :'static',
            'debug':False
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        text = self.get_argument("message", "来宾")
        self.render('index.html', ken=text)
        print("{'GET':'%s'}"%text)

    def post(self):
        text = self.get_argument("message")
        if text == "": text = "来宾"
        self.render('index.html', ken=text)

    def put(self):
        text = self.get_argument("message")
        if text == "": text = "None"
        self.write("{'Put':'%s'}"% text)

    def delete(self):
        self.write("delete: " + self.get_argument("message", "None"))

class BlogsHandler(tornado.web.RequestHandler):
    def get(self):
        res_list = []
        page_list=[]
        page_size = 5
        global page
        pag_num = self.get_argument('pag_num','0')
        page = page+int(pag_num)
        page_count=sql.cmd("select count(id) from blog")
        for i in page_count:
            page_count= int(i[0])
        if page <=0:
            page = 0
        elif page*page_size > page_count:
            page=page-1
        sqls="select * from blog where date order by date asc limit %s,%s"%(page*page_size,page_size)
        res = sql.cmd(sqls)
        res_list = [list(i) for i in res]
        res_list.reverse()
        self.render('blog.html', lists = res_list)

class BlogshowHandler(tornado.web.RequestHandler):
    def get(self,ids):
        res_list = []
        res = sql.cmd('select * from blog where id=%s;'% ids)
        res_list = [list(i) for i in res]
        self.render('blog.html', lists = res_list)

class BlogsflHandler(tornado.web.RequestHandler):
    def get(self,fl):
        res_list = []
        res = sql.cmd("select * from blog where fl='%s'"%fl)
        res_list = [list(i) for i in res]
        self.render('blog.html', lists = res_list)

class BlogaddHandler(tornado.web.RequestHandler):
    def get(self):
        res_list = []
        res = sql.cmd('select * from blog;')
        res_list = [list(i) for i in res]
        self.render('blog_add.html', lists = res_list)

    def post(self):
        res_list=[]
        ids = int(time.strftime("%Y%m%y%H%M%S")+ str(random.randrange(10000,99999)))
        name = 'admin'
        email = 'kkk@kkk.com'
        title = self.get_argument('title')
        fl = self.get_argument('fl')
        tag  = self.get_argument('tag')
        tms = time.strftime('%Y-%m-%d  %H:%M')
        content = self.get_argument('comment')
        for i in int(ids),name,email,title,fl,tag,tms,content:res_list.append(i)
        sql.cur.execute("insert into blog  values (?,?,?,?,?,?,?,?)",res_list)
        sql.commit()
        self.redirect('/test')

class BlogeditHandler(tornado.web.RequestHandler):
    def get(self,ids):
        res_list = []
        res = sql.cmd('select * from blog where id=%s;'% ids)
        res_list = [list(i) for i in res]
        self.render('blog_edit.html', lists = res_list)

    def post(self,ids):
        title = self.get_argument('title')
        fl = self.get_argument('fl')
        tag  = self.get_argument('tag')
        content = self.get_argument('comment')
        sql.cur.execute("update blog set title='%s',fl='%s',tag='%s',content='%s' where id = '%s'"%(
            title,fl,tag,content,ids))
        sql.commit()
        self.redirect('/test/%s'%ids)

class XmlHandler(tornado.web.RequestHandler):
    def get(self):
        res = sql.cmd('select * from blog;')
        res_list = [list(i) for i in res]
        self.render('xml.html',lists = res_list)

    def post(self):
        ids = self.get_argument('id_del')
        sql.cur.execute("delete from blog where id=%s"%ids)
        sql.commit()
        self.redirect('/xml')

class sqlHandler(tornado.web.RequestHandler):
    def get(self):
        countent = self.get_argument('comment','None')
        print('-------------',countent)
        self.render('uedit2.html',comment=countent)

class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        pass

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(myapp())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
