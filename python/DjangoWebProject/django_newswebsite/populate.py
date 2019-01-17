import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_newswebsite.settings')

import django
# 导入以上的项目设置
django.setup()
# 导入设置后才可导入项目中的模型
from news.models import Category, Page

# 根据一些数据测试模型是否正常运行
class TestData(object):
    def populate(self):
        fenghuangnews_pages = [
            {"title":"降税后个人工资反而下降？别拿问题数据忽悠人",
            "url":"http://news.ifeng.com/c/7fqHsHBvTNo", "views":10},
            {"title":"醒醒，苹果在华被禁售只是个法律问题",
            "url":"http://news.ifeng.com/c/7iYSj6gRHEG", "views":15},
            {"title":"视频报警短信报警均不靠谱，正确方法还是拨打110！",
            "url":"http://news.ifeng.com/c/7iYSj6gRHEG", "views":20},
        ]

        django_pages = [
            {"title":"database setup",
            "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial02/#database-setup", "views":25},
            {"title":"Playing with the API",
            "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial02/#playing-with-the-api", "views":30},
            {"title":"Enter the admin site",
            "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial02/#enter-the-admin-site", "views":35},
        ]

        other_pages = [
            {"title":"bilibili",
            "url":"https://www.bilibili.com/", "views":40},
            {"title":"github",
            "url":"https://github.com/Olaful?tab=repositories", "views":45},
            {"title":"CSDN",
            "url":"https://www.csdn.net/", "views":50},
        ]

        cates = {
            "fenghuangnews_pages":{"pages":fenghuangnews_pages},
            "Django":{"pages":django_pages},
            "Other":{"pages":other_pages}
        }

        def add_page(cate, title, url, views=0):
            # objects类似于数据库中的表的存储对象
            # 有则获取，没有则创建, 返回(object, created)
            # created 表示是否是新创建的模型实例
            p = Page.objects.get_or_create(category=cate, title=title)[0]
            p.url = url
            p.views = views
            p.save()
            return p

        def add_cates(name):
            c = Category.objects.get_or_create(name=name)[0]
            if name == 'fenghuangnews_pages':
                c.views = 128
                c.likes = 32
            elif name == 'Django':
                c.views = 64
                c.likes = 64
            elif name == 'Other':
                c.views = 32
                c.likes = 16
            c.save()
            return c

        # 根据模型添加数据库实例
        for cate, cate_data in cates.items():
            c = add_cates(cate)
            for p in cate_data['pages']:
                add_page(c, p['title'], p['url'], p['views'])

        for c in Category.objects.all():
            # filter过滤，还有count计算等类似数据库sql方法,
            for p in Page.objects.filter(category=c):
                print('- {0} - {1}'.format(str(c), str(p)))

    def updateView(self, name):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = 128
        c.save()

    def delete_cate(self, name):
        c = Category.objects.get(name=name)
        c.delete()

    def quey_cate(self, name):
        c = Category.objects.all()
        for c in c.values_list():
            print(c)

if __name__ == '__main__':
    print('Start News population script...')
    test_data = TestData()
    # test_data.populate()
    test_data.quey_cate('电影')