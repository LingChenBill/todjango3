from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# Create your views here.


def user_login(request):
    """
    用户登录view操作.
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 用户form实例化.
        form = LoginForm(request.POST)
        # 验证用户form.
        if form.is_valid():
            # 解析用户数据.
            cd = form.cleaned_data
            # 与DB用户数据验证.
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    # 若用户是激活的, 使用login方法将用户信息存入session.
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        # 初期化user form给用户登录画面.
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    """
    用户登录dashboard.
    login_required decorator检查当前用户是否经过身份验证.
    如果用户经过身份验证，则执行装饰视图;
    如果用户未通过身份验证，它会将用户重定向到登录URL，并将最初请求的URL作为名为next的GET参数.
    :param request:
    :return:
    """
    # 还可以定义一个section变量. 您将使用此变量跟踪用户正在浏览的站点部分.
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})
