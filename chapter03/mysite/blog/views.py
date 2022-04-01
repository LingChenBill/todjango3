from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from taggit.models import Tag
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


# Create your views here.


def post_list(request, tag_slug=None):
    """
    获取post列表, 过滤状态为published.
    添加特定tag的关联功能.
    :param request:
    :param tag_slug: 默认值为None, url中传tag的值.
    :return:
    """
    objects_list = Post.published.all()
    # 标签处理.
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # 一个post可以拥有多个tag, 一个tag可以从属于多个post.
        # 筛选tags. many to many关系.
        objects_list = objects_list.filter(tags__in=[tag])

    # 分页. 每页3个post.
    paginator = Paginator(objects_list, 3)
    # 获取当前页面数.
    page = request.GET.get('page')
    # print('page: ' + str(page))
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页面不是整数，则交付第一页.
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围，请提交最后一页结果.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


def post_detail(request, year, month, day, post):
    """
    获取post的详细信息.
    添加的post相关的comments信息.
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

    # 获取post相关的comments信息
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # 提交的comment处理.
        comment_form = CommentForm(data=request.POST)
        # 表单元素是否得到验证.
        if comment_form.is_valid():
            # 创建一个comment对象, 并不保存到db中.
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            # 保存到db.
            new_comment.save()
    else:
        # post页面初始时, 生成一个comment的form.
        comment_form = CommentForm()

    # 获取相似的posts.
    # 检索当前帖子标签的ID列表.
    # values_list是QuerySet返回带有给定项目值的元组.
    # 将flat=True传递给它，得到单个值，例如[1，2，3，…]而不是像[（1，），（2，），（3，）…]这样的一个元组.
    post_tags_ids = post.tags.values_list('id', flat=True)
    # 获取带这些的tag的posts, 排除自己.
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                                 .order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


def post_share(request, post_id):
    """
    通过id来检索post.
    :param request:
    :param post_id:
    :return:
    """
    # 通过ID检索到的具有"已发布"状态的post.
    post = get_object_or_404(Post, id=post_id, status='published')
    # 邮件发送成功flg.
    sent = False
    if request.method == 'POST':
        # 获取提交的email表单.
        form = EmailPostForm(request.POST)
        # 验证表单, 是否必入力, email是否正确等.
        if form.is_valid():
            # 获取表单数据.
            cd = form.cleaned_data
            # 发送Email....
            # post_url = request.build_absolute_url(post.get_absolute_url())
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # 邮件主题.
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            # 邮件信息
            message = f"Read {post.title} at {post_url} \n\n" \
                      f"{cd['name']} \'s comments: {cd['comments']}"
            # send_mail(subject, message, 'admin@admin.com', [cd['to']])
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


class PostListView(ListView):
    """
    1.使用特定的queryset，而不是检索所有对象.
    如果是queryset属性，则可以指定model=Post，Django将构建通用Post.objects.all().
    2.对查询结果使用上下文变量POST。默认变量是object_list
    3.如果您没有指定任何上下文对象名称对结果进行分页，每页显示三个对象使用自定义模板呈现页面.
    4.如果没有设置默认模板，ListView将使用blog/post_list.html.
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_search(request):
    """
    post的搜索接口.
    :param request:
    :return:
    """
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            # 提取query字段.
            query = form.cleaned_data['query']
            # 使用标题和正文字段构建的自定义SearchVector实例搜索已发布的posts.
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)

    return render(request, 'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
