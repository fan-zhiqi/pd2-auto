#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import time
from email.mime.text import MIMEText
from email.header import Header

sender = '251471915@qq.com'  # 发件人邮箱账号
my_pass = 'twcodhfinuvmbhad'  # 发件人邮箱密码
receivers = ['251471915@qq.com','linn403@163.com']  # 收件人邮箱账号，我这边发送给自己


def mail(url):

    try:
        now = time.strftime('%Y-%m-%d-%H-%M-%S')
        mail_msg = f'<p>报告结果访问{url}</p><p><a href={url}>这是一个链接，点击无法查看，请复制上面连接访问</a></p>'
        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['From'] = Header("AstaFan", 'utf-8')
        message['To'] = Header('', 'utf-8')

        subject = "pd2接口测试报告，执行时间{}".format(now)# 邮件的主题，也可以说是标题
        message['Subject'] = Header(subject, 'utf-8')

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender, receivers, message.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:
        print("邮件发送失败")
    return print("邮件发送成功")


