from django.conf.urls import url
from front import views

urlpatterns = [
    url(r'^login/',views.login,name='login'),
    url(r'^index/',views.index,name='index'),
    url(r'^register/',views.register,name='register'),
    url(r'^show_goods_info/(\d+)/',views.show_goods_info,name='show_goods_info'),
    url(r'^logout/',views.logout,name='logout'),
    url(r'^user_center_info/',views.user_center_info,name='user_center_info'),
    url(r'^cart/',views.cart,name='cart'),
    url(r'^user_center_order/',views.user_center_order,name='user_center_order'),
    url(r'^user_center_site/',views.user_center_site,name='user_center_site'),
    url(r'^add_cart/',views.add_cart,name='add_cart'),
    url(r'^place_older/',views.place_older,name='place_older'),
    url(r'^order/',views.order,name='order')

]