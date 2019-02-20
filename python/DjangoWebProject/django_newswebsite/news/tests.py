from django.test import TestCase
from news.models import Category, Page
from django.urls import reverse
import datetime

# Create your tests here.

# 测试category数据正确性，测试的时候会默认创建default空数据库，之后
# 可以把自己模型的数据填充到里面
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        "测试分类django的查看次数是否大于0，大于则返回True"
        cate = Category(name="Django", views=1, likes=0)
        # 需要在save方法中赋值views
        cate.save()
        self.assertEqual((cate.views >= 0), True)

    def test_slug_line_creation(self):
        "检查slug是否正确"
        cate = Category(name='first second three')
        cate.save()
        self.assertEqual(cate.slug, 'first-second-three')

def add_cate(name, views, likes):
        c = Category.objects.get_or_create(name=name)[0]
        c.views = views
        c.likes = likes
        c.save()
        return c

# 测试视图
class IndexViewTests(TestCase):
        # 测试页面数据
        def test_index_view_with_no_categories(self):
                # 通过client发送请求
                resp = self.client.get(reverse('index'))
                self.assertEqual(resp.status_code, 200)
                # 响应html中是否包含指定内容
                self.assertContains(resp, 'There are no categories present')
                # 响应对象上下文指定内容是否为空列表
                self.assertQuerysetEqual(resp.context['categories_top_like'], [])

        def test_index_view_with_categories(self):
                add_cate('test', 1, 1)
                add_cate('temp', 1, 1)
                add_cate('tmp', 1, 1)
                add_cate('tmp test temp', 1, 1)

                # default数据中已存在四个category的前提下，发送请求
                resp = self.client.get(reverse('index'))
                self.assertEqual(resp.status_code, 200)
                self.assertContains(resp, 'tmp test temp')

                cnt_cate = len(resp.context['categories_top_like'])
                self.assertEqual(cnt_cate, 4)

class PagesMethodTests(TestCase):
        # 第一次访问时间不等于将来时间
        def test_ensure_vistdate_no_future(self):
                cate = Category(name='Other')
                cate.save()
                page = Page(category=cate, title='github', url="http://123.com")
                page.save()
                self.assertEqual((page.first_visit <= datetime.datetime.now()), True)
                self.assertEqual((page.first_visit <= page.first_visit), True)