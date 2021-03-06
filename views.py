from django.shortcuts import render
from myblog.models import Post, Category
from django.core.paginator import Paginator
from markdown import Markdown
from django.db.models import Q, Count

# Create your views here.
POSTS_ONE_PAGE = 8


def index(request):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    all_article = Post.objects.all().order_by('-publish_data')
    all_types = Category.objects.all().annotate(numbers=Count('post')).order_by('-numbers')
    archives = Post.objects.all().values('publish_data__year').annotate(numbers=Count('*'))
    paginator = Paginator(all_article, POSTS_ONE_PAGE)
    page_num = paginator.num_pages
    page_articles_list = paginator.page(page)

    if page_articles_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_articles_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    top5_article_list = Post.objects.all().order_by('-views')[:5]
    return render(request, 'index.html', {
        'article_list': page_articles_list,
        'page_num': range(1, page_num + 1),
        'show_page': page_num,
        'curr_page': page,
        'next_page': next_page,
        'previous_page': previous_page,
        'top5': top5_article_list,
        'types': all_types,
        'archives': archives,
    })


def get_archive(request, year):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    all_article = Post.objects.filter(publish_data__year=year).order_by('-publish_data')
    all_types = Category.objects.all().annotate(numbers=Count('post')).order_by('-numbers')

    paginator = Paginator(all_article, POSTS_ONE_PAGE)  # 每一页10篇
    page_num = paginator.num_pages
    page_articles_list = paginator.page(page)
    archives = Post.objects.all().values('publish_data__year').annotate(numbers=Count('*'))

    if page_articles_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_articles_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    top5_article_list = all_article.order_by('-views')[:5]

    return render(request, 'tags.html', {
        'article_list': page_articles_list,
        'page_num': range(1, page_num + 1),
        'curr_page': page,
        'next_page': next_page,
        'previous_page': previous_page,
        'top5': top5_article_list,
        'types': all_types,
        'show_page': page_num,
        'archives': archives
    })


def get_tags(request, tag_id):
    page = request.GET.get('page')
    if page:
        page = int(page)
    else:
        page = 1
    cat = Category.objects.get(id=tag_id)
    all_article = Post.objects.filter(article_type=cat).order_by('-publish_data')
    all_types = Category.objects.all().annotate(numbers=Count('post')).order_by('-numbers')
    archives = Post.objects.all().values('publish_data__year').annotate(numbers=Count('*'))

    paginator = Paginator(all_article, 10)  # 每一页10篇
    page_num = paginator.num_pages
    page_articles_list = paginator.page(page)

    if page_articles_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_articles_list.has_previous():
        previous_page = page - 1
    else:
        previous_page = page
    top5_article_list = all_article.order_by('-views')[:5]

    return render(request, 'tags.html', {
        'article_list': page_articles_list,
        'page_num': range(1, page_num + 1),
        'curr_page': page,
        'next_page': next_page,
        'previous_page': previous_page,
        'top5': top5_article_list,
        'types': all_types,
        'show_page': page_num,
        'archives': archives,
    })


def search(request):
    search_content = request.GET.get("search_content")
    if not search_content:
        search_content = ''
    all_article = Post.objects.filter(
        Q(content__contains=search_content) |
        Q(title__contains=search_content) |
        Q(brief_content__contains=search_content)
    ).order_by('-views')
    all_types = Category.objects.all().annotate(numbers=Count('post')).order_by('-numbers')
    top5_article_list = all_article.order_by('-views')[:5]
    archives = Post.objects.all().values('publish_data__year').annotate(numbers=Count('*'))
    return render(request, 'search.html', {
        'article_list': all_article,
        'top5': top5_article_list,
        'types': all_types,
        'show_page': 1,
        'archives': archives,
    })


def get_detail_page(request, article_id):
    global curr_article
    articles = Post.objects.all().order_by("-publish_data")
    pre_index = 0
    next_index = 0
    for i, article in enumerate(articles):
        if article.article_id == article_id:
            curr_article = article
            article.increase_views()
            if i == 0:
                pre_index = 0
                next_index = i + 1
                if (len(articles) == 1):
                    next_index = i
            elif i == len(articles) - 1:
                next_index = i
                pre_index = i - 1
            else:
                pre_index = i - 1
                next_index = i + 1
            break
    md = Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    curr_article.content = md.convert(curr_article.content)
    return render(request, 'detail.html', {
        'curr_article': curr_article,
        'toc': md.toc,
        'previous_article': articles[pre_index],
        'next_article': articles[next_index],
    })
