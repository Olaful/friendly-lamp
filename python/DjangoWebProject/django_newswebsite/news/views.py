from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from news.models import Category, Page
from django.template import loader
from news.forms import CategoryForm, PageForm
from django.template.defaultfilters import slugify

# 函数就是一个视图，在urls文件添加映射
def index_test(request):
    # 视图必须返回一个HttpResponse对象
    # about前面不加/则以当前路径为父路径
    return HttpResponse('hello, welcome to news world! <a href="about">about</a>')

def index(request):
    # 使用关键字去填充模板中{{ keyworld }}中对应的内容,可以有多个
    # 关键字
    # context_dict = {'boldmessage':'Here are template world'}
    # 根据likes获取前五条数据, '-'表示反序
    category_list = Category.objects.order_by('-likes')[0:5]
    context_dict = {'categories_top_like':category_list}
    # top 5 点赞分类
    category_list = Category.objects.order_by('-views')[0:5]
    context_dict['categories_top_view'] = category_list
    # render函数也是返回HttpResponse对象
    # 这里就把视图，模板，模型的联系给建立起来了
    return render(request, 'news/index.html', context=context_dict)

    # 另一种渲染模板方式
    # temp = loader.get_template('news/index.html')
    # return HttpResponse(temp.render(context_dict, request))

def about_test(req):
    # /之前是域名
    return HttpResponse('more features, coming soon! <a href="/news">home</a>')

def about(request):
    context_dic = {}
    return render(request, 'news/about.html', context=context_dic)

def show_category(request, category_name_slug):
    context_dict = {}
    
    # 根据传入的分类名称查找数据库
    try:
        category = Category.objects.get(slug=category_name_slug)
        # 也可以使用此方式返回异常信息
        # category = get_object_or_404(Category, slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'news/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    # 是否是通过表单提交的请求
    if request.method == 'POST':
        # POST存放提交表单的数据，POST['name']返回的数据格式是字符串
        form = CategoryForm(request.POST)
        if form.is_valid:
            try:
                cate = form.save(commit=True)
                # 返回首页
                return index(request)
            except:
                # 发生错误时重定位到当前页面
                return render(request, 'news/add_category.html', {'form':form})
        else:
            print(form.errors)

    # get方式则显示原页面
    return render(request, 'news/add_category.html', {'form':form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid:
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category':category}
    return render(request, 'news/add_page.html', context_dict)