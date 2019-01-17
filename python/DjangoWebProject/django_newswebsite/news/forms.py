from django import forms
from news.models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    # 字段名称要与model定义的字段名称一样
    name = forms.CharField(max_length=Category.MAX_NAME_LEN,
                            help_text='Please input the category name.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # 与模型关联的字段,根据模型建立表单
        # 表单提交数据到模型对应的数据表中
        model = Category
        # 表单中包含的字段
        fields = ('name',) 

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text='Please input the title.')
    url = forms.URLField(max_length=200,
                            help_text='Please input the url.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        # 表单中不包含的字段
        exclude = ('category',)

    # 在save之前调用
    # 表单填写的数据是传递给cleaned_data的
    # 可以在clean方法中检查表单输入数据是否合理
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data
        
class UserForm(forms.ModelForm):
    # 覆盖User模型属性，改成密码组件样式
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')