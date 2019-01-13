from django import template
from news.models import Category

register = template.Library()

# 可在{{}}中或者{%%}中使用
@register.filter
def add_prefix(src, prefix):
    return str(prefix) + src

# 可在{%%}中使用，参数个数不限
@register.simple_tag
def catstr(str1, str2, str3):
    return str1 + str2 + str3

# 返回渲染后的html
@register.inclusion_tag('news/cates.html')
def get_category_list(cate=None):
    return {'cates': Category.objects.all(),
            'act_cate':cate}

