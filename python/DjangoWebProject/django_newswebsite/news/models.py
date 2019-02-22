from django.db import models
from django.utils import timezone
#from django.template.defaultfilters import slugify
from uuslug import slugify
from django.contrib.auth.models import User

import datetime

# 一个类对应一个模型, 模型对应数据库中的表
# 数据库类型不需要关心，因为ORM会自动根据
# 数据库类型生成对应的sql语句
# 这就是ORM对象关系映射
# 分类类，
class Category(models.Model):
    MAX_NAME_LEN = 128

    # 自定义字段，默认有id字段，用作主键，可以自定义修改
    name = models.CharField(max_length=MAX_NAME_LEN, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    # 其它字段, 字段名被重命名第一个参数，如果提供的话
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now())
    # 别名字段,标识每个模型实例
    slug = models.SlugField(unique=True)

    # 由于管理界面显示Categorys(默认),所以定义以下类进行更正
    # 元类，再次指定model类的配置，如表名称通过db_table
    # 指定，定义唯一主键等
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def is_outdate(self):
        return self.pub_date <= timezone.now() - datetime.timedelta(days=3)
    is_outdate.admin_order_field = 'pub_date'
    is_outdate.boolean = True
    # 字段显示名称
    is_outdate.short_description = 'outdate?'

    def save(self, *args, **kwargs):
        # slugify函数会把字符串中的空白符用'-'替换,大写变为小写
        self.slug = slugify(self.name)
        self.views = self.views
        super(Category, self).save(*args, **kwargs)

# 页面类
class Page(models.Model):
    # 一对多关系，还有OneToOneField一对一关系
    # ManyToManyField多对多关系
    # 会映射至Category的id字段，会自动创建索引
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    first_visit = models.DateTimeField(default=datetime.datetime.now())
    last_visit = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return self.title

# 用户模型扩展
class UserProfile(models.Model):
    # 建立与User模型之间的联系,User模型默认用username, password, email等属性
    # OneToOneField的话当前模型实例与User实例会同时被插入数据库
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # 额外增加的用户属性, 可以不填写(表单上)，但在设置日期，时间，数字类型时允许
    # 为空时应该同时设置null=True使用Null来存储空值
    website = models.URLField(blank=True)
    # profile_images文件夹会在media文件夹下建立
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

from django.db.models.signals import pre_save
from django.dispatch import receiver, Signal

mysig = Signal(providing_args=['arg1', 'arg2'])
mysig.send(sender='tbq', arg1='hello', arg2='world')

# 接收装饰器监听保存前发送的信号
@receiver(pre_save)
# 监听自定义信号发送函数发送的信号
# @receiver(mysig)
def my_callback(sender, **kwargs):
    print('保存前的操作')

class myAbsModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    
    class Meta:
        # 抽象model，指示该类不能创建数据表
        abstract = True

        ordering = ['name']

# 继承抽象model类，其中的字段名不能与基类相同
class TestModel(myAbsModel):
    address = models.CharField(max_length=100)

class Model1(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    other = models.IntegerField()
    # auto_now=True每次修改对象时会被自动更新为当前时间
    # auto_now_add=True以后修改对象时不会被更新
    createTime = models.DateTimeField(auto_now=True)

# 不会包含父类的字段，外键约束Model1的id
class Model2(Model1):
    address = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)

    class Meta:
        #  
        #app_label = 'hello'
        db_table = 'model22'
        # 有些数据库有表空间如oracle,可以指定表空间名称
        db_tablespace = 'ts'
        # 表不会被创建
        # managed = False
        # 唯一索引字段
        unique_together = ('address', 'mail')

class Model3(Model2):
    class Meta:
        # 使用代理，Model3与Model2操作的都是同一张表
        proxy = True

class Model4(Model2):
    # 多对多字段，会额外生成第三张表appname_model4_model1用以记录
    # 两个表之间的关系
    name = models.ManyToManyField('Model1')
    # 手动生成第三张表
    #name = models.ManyToManyField(to='Model1', through='Model42Model1', through_fields=('name', 'name'),)

def ModelOper():
    # 可以使用父表的字段进行查询，返回父表中的结果
    Model2.objects.filter(name='hello')

    # 创建子模型实例时会创建父模型实例，但建立父模型实例时不会创建子模型实例
    Model2.objects.create(name='hello', age=18, address='sz')

    from django.db.models import F, Q
    # F函数可以用作查询集中两个字段之间的比较
    # 且动态更改条件字段的值
    Model1.objects.filter(age_gt=F('other'))
    # 对字段进行操作
    Model1.objects.filter(age_gt=F('age')*2)

    # 使用Q构造复杂查询
    Model1.objects.filter(Q(name='mike')|Q(name='jack'))
    Model1.objects.filter(Q(name='mike')&Q(name='jack'))
    # 取反操作
    Model1.objects.filter(~Q(name='mike'))
    # 排除某列数据
    Model1.objects.defer('name')
    # 只取某列数据
    Model1.objects.only('name')

    from django.db.models import Count
    # 计算总个数
    Model1.objects.aggregate(k=Count('name'), distinct=True)
    # 获取条件之外的数据
    Model1.objects.exclude(name='mike')
    # 一次插入10条数据
    model_lsit = [Model1(name='mike'), Model1(name='jack')]
    Model1.objects.bulk_create(model_lsit, 10)