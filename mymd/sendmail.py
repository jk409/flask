__author__ = 'Administrator'
import smtplib
import email.mime.multipart
import email.mime.text
import time
def mails(smtp_server, port, username, passwd , mail_list, content):
        msg = email.mime.multipart.MIMEMultipart()
        #txt = email.mime.text.MIMEText(content)
        html = email.mime.text.MIMEText(content, 'html', 'utf-8')
        from_address = username
        to_address = mail_list
        msg['from'] = from_address
        msg['to'] = ','.join(to_address)
        msg['subject'] = '%s监控告警'%time.strftime("%Y-%m-%d_%H:%M")
        msg.attach(html)
        smtp = smtplib.SMTP()
        smtp.connect(smtp_server, port)
        smtp.login(username, passwd)
        smtp.sendmail(from_address, to_address, str(msg))
        smtp.close()
if __name__ == "__main__":
        mail_list = ['flyhu2009@q126.com']
        content = '''
                <p>%s<p>
                1234567890abcdefghijklmnopqrst
                1234567890abcdefghijklmnopqrstuvwxyz
                www.jk409.com'''%time.strftime("%Y-%m-%d_%H:%M")
        smtp_server = 'smtp.126.com'
        port = 25
        username = 'monitor_ser@126.com'
        passwd = '4854125'
        mails(smtp_server, port, username, passwd, mail_list, content)