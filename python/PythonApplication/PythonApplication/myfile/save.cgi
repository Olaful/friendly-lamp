#!F:\Users\ta\AppData\Local\Programs\Python\Python36\python.exe
#coding=utf-8

print('Content-type: text/html')

import cgi,cgitb,sys
from hashlib import sha1
from os.path import join, abspath

BASE_DIR = abspath('F:/httpd-2.4.37-o102p-x64-vc14/Apache24/cgi-bin')
form = cgi.FieldStorage()

text = form.getvalue('text')
filename = form.getvalue('filename')
password = form.getvalue('password')

# 校验参数
if not (filename and password and text):
    print('Invalid parameters')
    sys.exit()

# 校验密码,使用sha1能产生密码字符串的hash值,密码每改变一点，都会生成不同的密码摘要信息
if  (sha1(password.encode()).hexdigest()) != '2e8fcd939c82ff0cb6fae44a7b9e9298601068b5':
    print('Invalid password')
    sys.exit()

file = open(join(BASE_DIR, filename), 'w')
file.write(text)
file.close()

print('Success to save the file')
