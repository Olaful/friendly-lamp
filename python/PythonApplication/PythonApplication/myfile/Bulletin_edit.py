#!F:\Users\ta\AppData\Local\Programs\Python\Python36\python.exe
#coding=utf-8

import cgi,sys
import cgitb; cgitb.enable()
import psycopg2

conn = psycopg2.connect('user=tbq dbname=mypgdb')
cursor = conn.cursor()

form = cgi.FieldStorage()
reply_to = form.getvalue('reply_to')

print('Content-type: text/html\n')
print(
        """
        <html>
                <head>
                    <title>EditPage</title>
                </head>／
                <body>
                <h1>welcome to the Edit page</h1>
                <form action="save.cgi" method="POST">
        """
)

subject = ''

if reply_to is not None:
    # 获取回复的主题
    print('<input type="hidden" name="reply_to" value=%s>' % reply_to)
    cursor.execute('select subject from messages where id = %s' % reply_to)
    subject = cursor.fetchone()[0]
    if subject:
        subject = 'Re' + subject

print(
    # 回复格式：回复的主题，发送人，发送的消息
    """
    <b>Subject:</b>%s<br />
    <input type="text" size="40" name="sender" /><br >
    <b>Message:</b>
    <textarea name="text" cols="40" rows="20"></textarea><br />
    <input type="submit" value="Save" />
    </from>
    <hr />
    <a href="Bulletin_main.cgi">Back to the main page</a>
    </body>
    </html>
    """ % subject
)
