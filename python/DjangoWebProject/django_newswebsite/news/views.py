from django.shortcuts import render
from django.http import HttpResponse
from news.models import Category

# 函数就是一个视图，在urls文件添加映射
def index_test(request):
    # 视图必须返回一个HttpResponse对象
    # about前面不加/则以当前路径为父路径
    return HttpResponse('hello, welcome to news world! <a href="about">about</a>')

def index(request):
    # 使用关键字去填充模板中{{ keyworld }}中对应的内容
    #context_dict = {'boldmessage':'Here are template world'}
    # 根据likes获取前五条数据
    category_list = Category.objects.order_by('-likes')[0:5]
    context_dict = {'categories':category_list}
    # render函数也是返回HttpResponse对象
    # 这里就把视图，模板，模型的联系给建立起来了
    return render(request, 'news/index.html', context=context_dict)

def about_test(req):
    # /之前是域名
    return HttpResponse('more features, coming soon! <a href="/news">home</a>')

def about(request):
    context_dic = {}
    return render(request, 'news/about.html', context=context_dic)

