#!E:\Users\Administrator\AppData\Local\Programs\Python\Python36\python.exe
#coding=utf-8

import cgi,sys
import cgitb
cgitb.enable()
import psycopg2

conn = psycopg2.connect('user=tbq dbname=mypgdb')
cursor = conn.cursor()

form = cgi.FieldStorage()
id = form.getvalue('id')

try: id = int(id)
except:
    print("Invalid message id")
    sys.exit()

cursor.execute("select * from messages where id = %i" % id)

names = [d[0] for d in cursor.description]
rows = [dict(zip(names, row)) for row in cursor.fetchall()]

if not rows:
    print("Unknown message id:")
    sys.exit()

row = rows[0]

print('Content-type: text/html\n')
print(
        """
        <html>
                <head>
                    <title>ViewPage</title>
                </head>
                <body>
                <h1>welcome to the view page</h1>
        """
)

print(
    # 显示主题相关的文章内容
    """
    <p>
        <b>Subject:</b>%(subject)s<br />
        <b>Sender:</b>%(sender)s<br />
        <pre>%(text)s</pre>
    </p>
    <hr />
    <a href="Bulletin_main.cgi">Back to the main page<a/>
    <a href="Bulletin_edit.cgi?reply_to=%(id)s">Reply<a/>
    """ % row
)

