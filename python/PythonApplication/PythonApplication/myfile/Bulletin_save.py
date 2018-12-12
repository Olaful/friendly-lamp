#!F:\Users\ta\AppData\Local\Programs\Python\Python36\python.exe
#coding=utf-8

import cgi,sys
import cgitb; cgitb.enable()
import psycopg2

conn = psycopg2.connect('user=tbq dbname=mypgdb')
cursor = conn.cursor()

form = cgi.FieldStorage()

def quote(str):
    if str:
        return str.replace("'", "\\'")
    else:
        return str

subject = form.getvalue(quote('subject'))
sender = form.getvalue(quote('sender'))
text = form.getvalue(quote('text'))
reply_to = form.getvalue(quote('reply_to'))

if not (subject and sender and text):
    print("Please suply subject, sender, text")
    sys.exit()

if reply_to is not None:
    insertSql = """
        insert into messages(subject, sender, reply_to, text)
        value(%s, %s, %i, %s)
        """ % (subject, sender, int(reply_to), text)
else:
    insertSql = """
        insert into messages(subject, sender, text)
        value(%s, %s, %i, %s)
        """ % (subject, sender, text)

# 插入数据库并提交，否则将会丢失数据
cursor.execute(insertSql)
cursor.commit()

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