from django.conf.urls import url
from news import views

urlpatterns = [
    # Url传到这时，再次去掉news/部分，所以^$
    # 匹配空字符串能匹配到url
    # 如何匹配模式相同，则取第一个函数来处理
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name='about'),
]
