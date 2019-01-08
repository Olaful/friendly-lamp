from django.db import models

# 一个类对应一个模型,分类类
class Category(models.Model):
    # 自定义字段，默认有id字段，用作主键
    name = models.CharField(max_length=128, unique=True)

    # 由于管理界面显示Categorys(默认),所以定义一下类进行更正
    # 元类，再次指定model类的配置，如表名称通过db_table
    # 指定，定义唯一主键等
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# 页面类
class Page(models.Model):
    # 一对多关系，还有OneToOneField一对一关系
    # ManyToManyField多对多关系
    # 会映射至Category的id字段，会自动创建索引
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
