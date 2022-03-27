from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


# Create your views here.


def post_list(request):
    """
    获取post列表, 过滤状态为published.
    :param request:
    :return:
    """
    objects_list = Post.published.all()
    # 分页. 每页3个post.
    paginator = Paginator(objects_list, 3)
    # 获取当前页面数.
    page = request.GET.get('page')
    print('page: ' + str(page))
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页面不是整数，则交付第一页.
        print('No pages!')
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围，请提交最后一页结果.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts})


def post_detail(request, year, month, day, post):
    """
    获取post的详细信息.
    :param request:
    :param year:
    :param month:
    :param day:
    :param post:
    :return:
    """
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

