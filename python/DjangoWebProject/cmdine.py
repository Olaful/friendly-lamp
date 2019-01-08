from subprocess import Popen
import os

# 开启轻量级服务
start_server = 'python manage.py runserver 0.0.0.0:1025'
# 创建应用
create_app = 'python manage.py startapp news'
# 移除app数据模型
rm_appdata = 'python manage.py migrate news zero'

if __name__ == '__main__':
    os.chdir(r'DjangoWebProject/django_newswebsite')
    Popen(start_server, stdout = None, stderr = None, shell=True)