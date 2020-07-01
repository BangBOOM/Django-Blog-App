"""
author:Wenquan Yang
time:2020/6/30 20:14
"""
from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import Post


class AllPostsRssFeed(Feed):
    title = "BangBOOM Blog"

    link = "/"

    description = "BangBOOM"


    def items(self):
        return Post.objects.all()

    def item_title(self, item: Post):
        return "[%s] %s" % (item.article_type, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item: Post):
        return item.body_html

    def item_link(self, item):
        return reverse('myblog:get_detail', args=[item.article_id])
