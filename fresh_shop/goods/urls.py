from django.conf.urls import url
from goods import views

urlpatterns = [
    #  商品分类
    url(r'^goods_category_list/',views.goods_category_list,name='goods_category_list'),
    url(r'^goods_category_detail/(\d+)/',views.good_category_detail,name='good_category_detail'),
    url(r'^goods_list/',views.goods_list,name='goods_list'),
    url(r'^goods_add/',views.goods_add,name='goods_add'),
    url(r'^goods_del/(\d+)/',views.goods_del,name='goods_del'),
    url(r'^goods_edit/(\d+)/',views.goods_edit,name='goods_edit'),
    url(r'^goods_desc/(\d+)/',views.goods_desc,name='goods_desc'),
    url(r'^logout/',views.logout,name='logout')

]