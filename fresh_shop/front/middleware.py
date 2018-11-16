from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from goods.models import User
import re
from goods.models import ShoppingCart

class LoginMiddleware(MiddlewareMixin):

    def process_request(self,request):
        id = request.session.get('user_id')
        if id:
            user = User.objects.filter(pk=id).first()
            request.user = user
            return None
        not_check = ['/front/login/','/front/register/','/front/cart/','/front/index/','/front/show_goods_info/(.*)/',
                     '/front/add_cart/','/back/*/','/goods/*/']
        path = request.path
        for not_path in not_check:
            if re.match(not_path,path):
                return None
        return HttpResponseRedirect(reverse('front:login'))

    # 访问页面跳转到登录，但不能加载，提示302重定向次数过多


class SessionUpdate(MiddlewareMixin):
    def process_request(self,request):
        # session中商品数据和购物车表中数据的同步操作
        # session中数据结构[[goods_id,goods_num,goods_status]....]
        session_goods = request.session.get('goods')
        user_id = request.session.get('user_id')
        if user_id:
            if session_goods:
                # 同步数据库数据和session数据
                # 如果session中商品已经存在数据库表中，则更新，不存在，添加
                for goods in session_goods:
                    # goods的结构[id,num,is_select]
                    cart = ShoppingCart.objects.filter(user_id=user_id,goods_id=goods[0]).first()
                if cart:
                    # 数据库中能查询到该商品信息，则修改
                    cart.nums = goods[1]
                    cart.is_select = goods[2]
                    cart.save()
                else:
                    # 查询不到数据，添加
                    ShoppingCart.objects.create(user_id=user_id,goods_id=goods[0],nums=goods[1],is_select=goods[2])
        # 如果session中的数据少于购物车表的数据，同步数据库到session
        carts = ShoppingCart.objects.filter(user_id=user_id).all()
        session_new_goods = [[cart.goods_id,cart.nums,cart.is_select] for cart in carts]
        request.session['goods'] = session_new_goods
        return None












































