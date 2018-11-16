from django.conf.urls import url
from back import views
urlpatterns = [
    # 登录
    url(r'login/',views.login,name='login'),
    url(r'index/',views.index,name='index'),

]