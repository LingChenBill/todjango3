from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_action

# Create your views here.


@login_required
def image_create(request):
    """
    图片创建view.
    """
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)

            # 将图片绑定用户.
            new_item.user = request.user
            new_item.save()

            # 储存图片创建操作.
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully.')

            # 将用户重定向到新图像的规范URL. 你还没有实现了图像模型的get_absolute_url()方法, 你会以后再做.
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    """
    图片详细信息.
    :param request:
    :param id:
    :param slug:
    :return:
    """
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image})


@ajax_required
@login_required
@require_POST
def image_like(request):
    """
    图片喜爱/不喜爱操作.
    需要登录的装饰器阻止未登录的用户访问此视图.
    如果HTTP请求没有通过POST完成，require_POST decorator将返回一个HttpResponseNotAllowed对象（状态代码405）.
    这样，您只允许对该视图进行POST请求。
    :param request:
    :return:
    """
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                # 储存用户like操作.
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})

        except:
            pass

    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    """
    图片列表.
    :param request:
    :return:
    """
    images = Image.objects.all()
    # 构建Paginator对象对结果进行分页，每页检索八幅图像.
    paginator = Paginator(images, 8)
    page = request.GET.get('page')

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # 若请求是一个ajax, 且页码超过界限, 返回一个空的对象.
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    if request.is_ajax():
        # 这个模板将只包含请求页面的图像.
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images',
                       'images': images})

    # 这个模板将扩展base.html模板来显示整个页面，并将包括list_ajax.html模板, 用来包括图像列表.
    return render(request,
                  'images/image/list.html',
                  {'section': 'images',
                   'images': images})

