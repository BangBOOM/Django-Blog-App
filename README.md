# 这是一个基于Django和Bootstrap的个人博客APP

这是一个比较简洁的博客会持续更新修改

样式直接访问这个[DEMO](https://justyan.top/blog/index)

此项目基于Django3.0开发
settings和url中的设置
```Python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mdeditor',
    'myblog',
]

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from MyWebSite import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.index),
                  path('blog/', include('myblog.urls', namespace='blog')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

特别提醒代码高亮的部分只需要Markdown库不需要Pygments（安装了需要删除）见[link](https://justyan.top/blog/detail/22)

