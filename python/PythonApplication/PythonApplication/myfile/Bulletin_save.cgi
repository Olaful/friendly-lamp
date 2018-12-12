#!E:\Users\Administrator\AppData\Local\Programs\Python\Python36\python.exe
#coding=utf-8

print('Content-type: text/html\n')

import cgi,sys
import cgitb
# 输出错误追踪日志到浏览器；不输出到目录；显示错误信息上下文五条；显示格式为html
cgitb.enable(display=1, logdir=None, context=5, format="html")
import psycopg2

conn = psycopg2.connect('user=tbq dbname=mypgdb')
cursor = conn.cursor()

form = cgi.FieldStorage()

def quote(str):
    if str:
        return str.replace("'", "\\'")
    else:
        return str

subject = quote(form.getvalue('subject'))
sender = quote(form.getvalue('sender'))
text = quote(form.getvalue('text'))
reply_to = quote(form.getvalue('reply_to'))

if not (subject and sender and text):
    print("Please suply subject, sender, text")
    sys.exit()

if reply_to is not None:
    insertSql = """
        insert into messages(subject, sender, reply_to, text)
        values('%s', '%s', %i, '%s')
        """ % (subject, sender, int(reply_to), text)
else:
    insertSql = """insert into messages(subject, sender, text) values('%s', '%s', '%s')""" % (subject, sender, text)
		
# 插入数据库并提交，否则将会丢失数据
cursor.execute(insertSql)
conn.commit()

print(
    """
        <html>
                <head>
                    <title>SavePage</title>
                </head>／
                <body>
                <h1>Message saved</h1>
                <hr />
                <a href="Bulletin_main.cgi">Back to the main page</a>
    """
)