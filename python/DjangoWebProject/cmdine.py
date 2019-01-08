from subprocess import Popen
import os

# 开启轻量级服务
start_server = 'python manage.py runserver 0.0.0.0:1025'
# 创建应用
create_app = 'python manage.py startapp news'
# 创建数据库 默认sqlite3数据库,之后应用的更新就可以同步到
# 各自的数据库，如果有待提交的sql数据，则是提交数据至数据库
create_or_up__appdata = 'python manage.py migrate'
# 移除app数据模型
rm_appdata = 'python manage.py migrate news zero'
# 创建数据库超级用户
create_superuser = 'python manage.py createsuperuser'
# 生成模型数据的迁移sql，在应用目录的 migrations目录下面
# 会生成更新信息
gener_sql = 'python manage.py makemigrations news'
# 查看某个应用数据迁移至数据库的sql
see_sql = 'python manage.py sqlmigrate news 0001'
# 打开shell,shell常用于调试项目
shell = 'python manage.py shell'

if __name__ == '__main__':
    os.chdir(r'DjangoWebProject/django_newswebsite')
    Popen(start_server, stdout = None, stderr = None, shell=True)