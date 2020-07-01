import re
import markdown
from django.db import models
from django.utils.functional import cached_property
from markdown.extensions.toc import TocExtension, slugify
from mdeditor.fields import MDTextField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    # 唯一ID
    article_id = models.AutoField(primary_key=True)
    # 文章类型
    article_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 文章标题
    title = models.CharField(max_length=50)
    # 摘要
    brief_content = models.TextField()
    # 主要内容
    content = MDTextField()
    # 发布日期
    publish_data = models.DateTimeField(auto_now=True)
    # 阅读量
    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        try:
            self.views += 1
        except:
            self.views = 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.content)


def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}
