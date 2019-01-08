import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_newswebsite')

import django
django.setup()
from news.models import Category, Page

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