"""
Django settings for django_newswebsite project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kjr#jbw&+d^s!0n@_f3pz!)p29xl$d$6iy7v8%h*k3ksy-=zw6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.123.175', '127.0.0.1', 'localhost', 'senkie.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册自己的应用
    'news',
    # 使用第三方用户管理模块，注册，登录，注销，验证等功能
    'registration',
    'bootstrap_toolkit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 会话处理中间件
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# registration应用的设置信息
# 是否允许注册
REGISTRATION_OPEN = True
# 注册后有剩余多久可以激活
ACCOUNT_ACTIVATION_DAYS = 3
# 注册后是否自动登录
REGISTRATION_AUTO_LOGIN = True
# 登录后页面
LOGIN_REDIRECT_URL = '/news/'
# 访问需要登录的页面或者未登录重定向的页面
LOGIN_URL = '/accounts/login/'
# 自定义注册表单
#REGISTRATION_FORM = 'news.forms.UserProfileForm'

# 启用浏览器存续期会话(浏览器关闭后会话过期),默认使用持久性会话，由服务器
# 决定会话过期时间
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 持久性会话过期时间,单位秒
SESSION_COOKIE_AGE = 3600

ROOT_URLCONF = 'django_newswebsite.urls'

TEMPLATES = [
    {
        # 使用DTL模板渲染系统
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 使用绝对路径，以下路径中的模板将由BACKEND指定的模板系统来渲染
        'DIRS': [TEMPLATE_DIR, ],
        # 可以查找APP中的模板
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 上传的媒体文件有该processors处理
                'django.template.context_processors.media',
            ],
        },
    },
    # {
    #     'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #     # 其他由Jinja2渲染系统渲染的模板路径
    #     'DIRS': [],
    # }
]

WSGI_APPLICATION = 'django_newswebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 默认使用sqlite3数据库引擎，也可以使用其它数据库引擎如postgresql
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 如果使用其它需要认证的数据库，则配置如下信息
        # USER 
        # PASSWORD
        # HOST
        # PORT
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

# 密码有效性验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # 限定密码最小长度
        'OPTIONS':{'min_length':6,},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 使用以下算法加密用户密码，默认第一个，无效的话使用第二个
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
)


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-Hans'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Hong_Kong'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [STATIC_DIR,]

MEDIA_ROOT = MEDIA_DIR
# 路径后面要加上斜线,因为该路径下面可能还有其他路径
MEDIA_URL = '/media/'

# 登录装饰器把未登录的用户的访问请求重定向到该地址
LOGIN_URL = '/news/login/'