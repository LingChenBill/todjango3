from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image

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

