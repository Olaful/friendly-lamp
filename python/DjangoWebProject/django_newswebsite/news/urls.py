from django.conf.urls import url
from news import views

# 命名空间名称,之后模板中中的url可以使用
# userpace:urlname代替，命令空间可以有效
# 区分url名称所属的区域，
app_name = 'news'
urlpatterns = [
    # Url传到这时，再次去掉news/部分，所以^$
    # 匹配空字符串能匹配到url
    # 如何匹配模式相同，则取第一个函数来处理
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name='about'),
    # 正则匹配的()中的内容会当作参数与request参数一起传给对应的视图，
    # ?P<paramname>指定参数名，如果有参数，参数一定得传入
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^search/$', views.search, name="search"),
    url(r'^userinfo/$', views.userinfo, name="user_info"),
    url(r'^userinfo/(?P<user_name>[\w\d]+)/$', views.personalinfo, name="personal_info")
    # url(r'^register/$', views.register, name='register'),
    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout/$', views.user_logout, name='logout'),
]
