from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from utils.forms import UserLoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def login(request):
    if request.method == 'GET':
        # get请求返回登录页面
        return render(request,'back/login.html')
    if request.method == 'POST':
        # 将请求的参数丢给form表单做校验
        form = UserLoginForm(request.POST)
        # 校验结果，返回True表示检验成功
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))
            if user:
                # request.user赋值，赋值为登录对象，request.user等于系统用户对象
                auth.login(request, user)
                return HttpResponseRedirect(reverse('back:index'))
            else:
                # 没有user对象
                return render(request, 'login.html')
        else:
            return render(request, 'login.html', {'errors': form.errors})

@login_required
def index(request):
    if request.method == 'GET':
        return render(request,'back/index.html')