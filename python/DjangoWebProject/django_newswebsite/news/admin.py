from django.contrib import admin
from news.models import Category, Page

# 继承ModelAdmin自定义管理界面
class myAdmin(admin.ModelAdmin):
    list_filter=('publication_date',)

# 注册后才能在管理界面看到模型信息
admin.site.register(Category)
admin.site.register(Page)
# 用myAdmin定义的界面管理 Category
#admin.site.register(Category,myAdmin)
