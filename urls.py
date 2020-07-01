"""
author:Wenquan Yang
time:2020/6/30 12:54
"""
from django.urls import path
from myblog import views
from myblog.feeds import AllPostsRssFeed

app_name = "myblog"

urlpatterns = [
    path("index", views.index, name="index"),
    path("detail/<int:article_id>", views.get_detail_page, name="get_detail"),
    path("tag/<int:tag_id>", views.get_tags, name="get_tag"),
    path("search/", views.search, name="search"),
    path("rss/", AllPostsRssFeed(), name="rss"),
]
