"""django_newswebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from news import views

urlpatterns = [
    # path('index/', views.index),
    # ^$开头至结尾匹配url,交给指定的函数进行处理，name参数可选
    # name在模板中可以代替指定url路径
    url(r'^$', views.index, name='index'),
    # url路径去掉域名后剩下的news路径交由指定应用的urls来处理
    url(r'^news/', include('news.urls')),
    # 传给下一个urls处理时去掉news/about/路径部分
    #url(r'^news/about/', include('news.urls')),
    # 管理员界面，用于管理模型等
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
