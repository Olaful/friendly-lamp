#!E:\Users\Administrator\AppData\Local\Programs\Python\Python36\python.exe
#coding=utf-8

print('Content-type: text/html')

import cgi,cgitb,sys
from os.path import join, abspath

BASE_DIR = abspath('D:/Apache24/cgi-bin')

# 通过关键字获取表单提交的数据(url中的请求参数)
# 如何没有获取到数据，则读取原文件的内容用于显示在textarea中
form = cgi.FieldStorage()
filename = form.getvalue('filename')

if not filename:
    print('Please enter a filename')
    sys.exit()

text = open(join(BASE_DIR, filename), encoding='utf-8').read()

print(
"""
<html>
        <head>
            <title>EditPage</title>
        </head>
		 <body>
		 <h1>welcome to the edit page</h1>
        <!--数据量较大时使用POST方法，其不会在url中显示参数，form提交会将form中的数据送入url参数中-->
        <form action="save.cgi" method="POST">
        <b>File:</b> %s</br>
        <input type="hidden" value="%s" name="filename" />
        <b>Password:</b></br>
        <input type="password" name="password"></br>
        <b>Text:</b></br>
        <textarea rows='10' cols='20' name="text">%s</textarea><br/>
        <input type="submit" value="保存" />
        </form>
    </body>
</html>
""" % (filename, filename, text)
)