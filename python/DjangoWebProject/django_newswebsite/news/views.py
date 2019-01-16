from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from news.models import Category, Page
from django.template import loader
from news.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.template.defaultfilters import slugify
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from news.webhose_search import run_query
from news.webdriver_search import WebDriver, BrowserRender
from django.contrib.auth.models import User

# 返回HttpResponse的对象的函数就是一个视图，在urls文件添加映射
def index_test(request):
    # 视图必须返回一个HttpResponse对象
    # about前面不加/则以当前路径为父路径
    return HttpResponse('hello, welcome to news world! <a href="about">about</a>')

def index(request):
    CookieChk(request, 'sessionid')
    # 使用关键字去填充模板中{{ keyworld }}中对应的内容,可以有多个
    # 关键字
    # context_dict = {'boldmessage':'Here are template world'}
    # 根据likes获取前五条数据, '-'表示反序
    category_list = Category.objects.order_by('-likes')[0:5]
    context_dict = {'categories_top_like':category_list}
    # top 5 点赞分类
    category_list = Category.objects.order_by('-views')[0:5]
    context_dict['categories_top_view'] = category_list
    # render函数也是返回HttpResponse对象,内部调用 render_to_string函数
    # 这里就把视图，模板，模型的联系给建立起来了

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    resp = render(request, 'news/index.html', context=context_dict)

    return resp

    # 另一种渲染模板方式
    # temp = loader.get_template('news/index.html')
    # return HttpResponse(temp.render(context_dict, request))

def about_test(req):
    # /之前是域名
    return HttpResponse('more features, coming soon! <a href="/news">home</a>')

def about(request):
    # 测试cookie是否可用
    if request.session.test_cookie_worked():
        print('TEST COOKIE WORKED')
        request.session.delete_test_cookie()

    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    # reuqest中带有用户请求的相关信息
    #print(request.method, request.user)
    return render(request, 'news/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    
    # 根据传入的分类名称查找数据库
    try:
        category = Category.objects.get(slug=category_name_slug)
        # 查看次数加1
        category.views += 1
        category.save()
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

    # 用户是否登录
    # if not request.user.is_authenticated():
    #     return HttpResponse("请先登录")

    # 是否是通过表单提交的请求
    if request.method == 'POST':
        # POST存放提交表单的数据，POST['name']返回的数据格式是字符串
        form = CategoryForm(request.POST)
        if form.is_valid:
            try:
                # commit提交事务
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

# 登录装饰器检查登录，如果未登录，则重定向到LOGIN_URL
@login_required
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

def register(request):
    # 是否注册成功
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # 生成密码哈希值
            user.set_password(user.password)
            user.save()

            # 因为要处理user属性，所以暂时不提交，以防出现完整性问题
            profile = profile_form.save(commit=False)
            profile.user = user

            # 获取提供的头像数据
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        # 表单数据校验不通过
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # 非POST请求，设置空表单
        user_form = UserForm()
        profile_form = UserProfileForm()

    content_dict = {'user_form':user_form, 'profile_form':profile_form, 'registered':registered}
    return render(request, 'news/register.html', content_dict)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate函数进行验证
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                # 登录成功后重定向到首页，返回码302
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("你的News账户未激活")
        else:
            print("Invalid login detail:{0}, {1}".format(username, password))
            # return HttpResponse("无效的登录信息")
            return render(request, 'news/login.html', {'error':"无效的用户名或密码，请重新输入..."})
    else:
        return render(request, 'news/login.html', {})                

# 只有登录用户能访问这个视图
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def visitor_cookie_handler(request):
    # 从cookie中获取网站的访问次数与访问时间
    # cookie存储的都是字符串
    # visits = int(request.COOKIES.get('visits', '1'))
    # last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.datetime.now()))
    # 从会话中读取cookie，会话退出后，cookie数据也会被重置
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.datetime.now()))
    last_visit_time = datetime.datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # 以5分钟为单位统计访问次数
    if (datetime.datetime.now() - last_visit_time).seconds > 300:
        visits += 1
        # 向响应中设置数据，这样客户端就能知道cookie对应的值,
        # 如果cookie不存在，则会创建，不过cookie最好不放在
        # 请求中返回，因为这样会在客户端中暴露cookie信息
        # 由服务器端从会话中获取并渲染显示在返回的html中较好
        # response.set_cookie('last_visit', str(datetime.datetime.now()))
        request.session['last_visit'] = str(datetime.datetime.now())
    else:
        # response.set_cookie('last_visit', last_visit_cookie)
        request.session['last_visit'] = last_visit_cookie

    # response.set_cookie('visits', visits)
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# 检查cookie
def CookieChk(request, cookieName):
    # 测试cookie功能是否可用
    request.session.set_test_cookie()
    # 检查指定的cookie是否存在于客户端浏览器中
    is_cookie_exist = False if request.COOKIES.get(cookieName) is None else True
    # 指定的cookie是否位于服务器中
    # is_cookie_exist = False if request.session.get('last_visit') is None else True
    if is_cookie_exist:
        print('the cookie {} value is {}'.format(cookieName, request.COOKIES[cookieName]))
    else:
        print('{} is not exist:'.format(cookieName))

# 通过webhose搜索视图
def search_webhose(request):
    rls_list = []
    query = ""
    if request.method == "POST":
        query = request.POST['query'].strip()
        if query:
            rls_list = run_query(query)
    return render(request, 'news/search.html', {'result_list': rls_list, 'query_word':query})

# 获取百度搜索结果
def search(request):
    rls_list = []
    query = ""
    if request.method == "POST":
        br = WebDriver()
        query = request.POST['query'].strip()
        if query:
            rls_list = br.run_query(query)
    return render(request, 'news/search.html', {'result_list': rls_list, 'query_word':query})

# 用户列表
def userinfo(request):
    userinfo = User.objects.all()
    return render(request, 'news/userinfo.html', {'userinfo': userinfo})

# 个人信息
def personalinfo(request, user_name):
    userinfo = User.objects.get_by_natural_key(username=user_name)
    return render(request, 'news/personalinfo.html', {'userinfo': userinfo})

def track_url(request, name='goto', page_id=None):
    page = Page.objects.get(id=page_id)
    if page_id is None or page is None:
        return HttpResponseRedirect(reverse('index'))

    page.views += 1
    page.save()

    # 重定向到page真正的url
    return redirect(page.url)

    #return redirect('/index/')
    
