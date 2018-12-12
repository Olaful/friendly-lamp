#!F:\Users\ta\AppData\Local\Programs\Python\Python36\python.exe
#coding=utf-8
import cgi
import cgitb; cgitb.enable()
import psycopg2

conn = psycopg2.connect('user=tbq dbname=mypgdb')
cursor = conn.cursor()
cursor.execute('select * from messages')

names = [d[0] for d in cursor.description]
# 拼接成[{colname:value},{colname:value}]的形式
rows = [dict(zip(names, row)) for row in cursor.fetchall()]

print('Content-type: text/html\n')
print(
        """
        <html>
                <head>
                    <title>MainPage</title>
                </head>
                <body>
                <h1>welcome to the main page</h1>
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
    #print(row['subject'])
    # 主题链接到文章，文章页面会先根据传入的主题id去取数据库的数据显示出来
    print('<p><a href="Bulletin_view.cgi?id=%(id)i">%(subject)s</a></p>' % row)
    try: kids = children[row['id']]
    except KeyError: pass
    else:
        print('<blockquote>')
        for kid in kids:
            # 递归打印回复的消息
            format(kid)
        print('</blockquote>')

print('<p>')

for row in toplevel:
    format(row)

print(
        """
        </p>
        <!--创建一条水平分割线-->
        <hr />
        <p><a href="Bulletin_edit.cgi">write new message</a></p>
        </body>
        </html>
        """
)
