#!E:\Users\Administrator\AppData\Local\Programs\Python\Python36\python.exe
#coding=utf-8
import cgi
import cgitb; cgitb.enable()

print('Content-type: text/html\n')
import psycopg2
conn = psycopg2.connect('user=tbq dbname=mypgdb')
cursor = conn.cursor()
cursor.execute('select * from messages')
names = [d[0] for d in cursor.description]
rows = [dict(zip(names, row)) for row in cursor.fetchall()]

print(
"""
<html>
        <head>
            <title>EditPage</title>
        </head>
        <body>
        <h1>welcome to the edit page</h1>
"""
)

toplevel = []
children = {}

for row in rows:
    parent_id = row['reply_to']
    if parent_id is None:
        toplevel.append(row)
    else: children.setdefault(parent_id, []).append(row)

def format(row):
    print(row['subject'])
    try: kids = children[row['id']]
    except KeyError: pass
    else:
        print('<blockquote>')
        for kid in kids:
            format(kid)
        print('</blockquote>')

print('<p>')

for row in toplevel:
    format(row)

print(
"""
</p>
</body>
</html>
"""
)
