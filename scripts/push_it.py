# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import date


def push_sig(title, error_info=''):
    sender = 'xx@xx.com'
    receiver = 'xxxx@xx.com'
    receiver_peng = 'xxx@xx.com'
    subject = '%s' % title
    smtpserver = 'smtp.xx.com'
    username = 'xxx@xx.com'
    password = 'password'

    msg = MIMEText(error_info, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect('smtp.xx.com')
    smtp.login(username, password)
    smtp.sendmail(sender, receiver_peng, msg.as_string())
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    push_sig('买入信号', '啦啦啦啦 ~\(≧▽≦)/~啦啦啦')
