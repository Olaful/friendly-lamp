from django.conf.urls import url
from news import views

urlpatterns = [
    # Url传到这时，再次去掉news/部分，所以^$
    # 匹配空字符串能匹配到url
    # 如何匹配模式相同，则取第一个函数来处理
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name='about'),
    # 正则匹配的()中的内容会当作参数与request参数一起传给对应的视图，
    # ?P<paramname>指定参数名
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
]
