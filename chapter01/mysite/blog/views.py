from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.


def post_list(request):
    """
    获取post列表, 过滤状态为published.
    :param request:
    :return:
    """
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


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

