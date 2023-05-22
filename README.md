# 这是一个基于Django和Bootstrap的个人博客APP



## 当前功能

- [x] 文章详情页面
- [x] 文章列表
- [x] 按类别分类
- [x] 全局关键字搜索
- [x] 详情页面美化
- [x] 归档页面
- [ ] 评论，准备做个第三方集成
- [ ] 给文章可以设置多类别
- [ ] css代码部分标准化



这是一个基于Django的个人博客APP，使用的时候直接加入到新建的django项目中，settings文件的配置如下

样式直接访问这个[DEMO](https://site.bangboom.nl/blog/index)

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

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('blog/', include('myblog.urls', namespace='blog')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

特别提醒代码高亮的部分只需要Markdown库不需要Pygments（安装了需要删除）见[link](https://justyan.top/blog/detail/22)

