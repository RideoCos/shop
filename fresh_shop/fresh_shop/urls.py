"""fresh_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.staticfiles.urls import static

from fresh_shop.settings import MEDIA_ROOT,MEDIA_URL
from utils.upload_images import upload_image

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^back/',include('back.urls',namespace='back')),
    url(r'^goods/',include('goods.urls',namespace='goods')),
    # 编辑器上传路由
    url(r'^util/upload/(.*)',upload_image),
    url(r'^front/',include('front.urls',namespace='front')),


]

# 解析图片

urlpatterns += static(MEDIA_URL,document_root=MEDIA_ROOT)