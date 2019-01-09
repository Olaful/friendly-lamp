import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_newswebsite.settings')

import django
# 导入以上的项目设置
django.setup()
# 导入设置后才可导入项目中的模型
from news.models import Category, Page

# 根据一些数据测试模型是否正常运行
def populate():
    fenghuangnews_pages = [
        {"title":"降税后个人工资反而下降？别拿问题数据忽悠人",
        "url":"http://news.ifeng.com/c/7fqHsHBvTNo"},
        {"title":"醒醒，苹果在华被禁售只是个法律问题",
        "url":"http://news.ifeng.com/c/7iYSj6gRHEG"},
        {"title":"视频报警短信报警均不靠谱，正确方法还是拨打110！",
        "url":"http://news.ifeng.com/c/7iYSj6gRHEG"},
    ]

    django_pages = [
        {"title":"database setup",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial02/#database-setup"},
        {"title":"Playing with the API",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial02/#playing-with-the-api"},
        {"title":"Enter the admin site",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial02/#enter-the-admin-site"},
    ]

    other_pages = [
        {"title":"bilibili",
        "url":"https://www.bilibili.com/"},
        {"title":"github",
        "url":"https://github.com/Olaful?tab=repositories"},
        {"title":"CSDN",
        "url":"https://www.csdn.net/"},
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
            add_page(c, p['title'], p['url'])

    for c in Category.objects.all():
        # filter过滤，还有count计算等类似数据库sql方法,
        for p in Page.objects.filter(category=c):
            print('- {0} - {1}'.format(str(c), str(p)))

if __name__ == '__main__':
    print('Start News population script...')
    populate()