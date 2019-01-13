from django.contrib import admin
from news.models import Category, Page, UserProfile

class PagesInline(admin.StackedInline):
    model = Page
    # 默认显示的待添加page数量
    #extra = 3

# 一行数据一行显示
class PagesSingleInline(admin.TabularInline):
    model = Page
    # 默认显示的待添加page数量
    extra = 3

# 继承ModelAdmin自定义管理界面
class CategoryAdmin(admin.ModelAdmin):
    # 列头
    list_display = ('name', 'pub_date', 'views', 'likes', 'is_outdate', 'slug')

    # 过滤器字段
    list_filter = ['pub_date']

    # 搜索字段, 后台sql查询将使用like '%name%'来查询
    search_fields = ['name']

    # 分页, 数量大于此数字才显示分页效果
    list_per_page = 10

    # 字段显示顺序
    # fields = ['name', 'views', 'likes']
    # 字段分组显示
    fieldsets = [
        (None, {'fields':['name', 'pub_date', 'slug']}),
        ('欢迎程度', {'fields':['views', 'likes']})
    ]

    # 在当前模型实例下显示其它模型实例
    inlines = [PagesSingleInline]

    # 根据某字段自动填写
    prepopulated_fields = {'slug':('name',)}

class PagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')    
    list_per_page = 10

# 注册后才能在管理界面看到模型信息
#admin.site.register(Category)
admin.site.register(Page, PagesAdmin)
# 用myAdmin定义的界面管理 Category
admin.site.register(Category,CategoryAdmin)
admin.site.register(UserProfile)