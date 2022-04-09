from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from common.decorators import ajax_required

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


def register(request):
    """
    用户注册.
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            # 保存用户输入的原始密码时，可以使用处理哈希的用户模型的set_password()方法.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # 用户配置信息.
            Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    """
    用户编辑view设置.
    UserEditForm用于存储内置用户模型的数据，ProfileEditForm用于在自定义配置文件模型中存储附加的profile数据.
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # 信息设置.
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Error updating your profile.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    """
    获取用户列表.
    :param request:
    :return:
    """
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    """
    用户详细信息.
    :param request:
    :param username:
    :return:
    """
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)

    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    """
    用户follow操作. POST提交数据.
    :param request:
    :return:
    """
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})

