from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from front.forms import UserRegisterForm,UserLoginForm,AddressForm
from goods.models import User,Goods,GoodsCategory,UserAddress,ShoppingCart,OrderGoods,OrderInfo
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse


# 登录页面
def login(request):
    if request.method == 'GET':
        return render(request,'web/login.html')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data.get('username')).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('front:index'))
        else:
            return render(request,'web/login.html',{'errors':form.errors})


# 首页显示
def index(request):
    if request.method == 'GET':
        goods = Goods.objects.all()
        types = GoodsCategory.CATEGORY_TYPE
        user = request.user
        goods_dict = {}
        for type in types:
            goods_list = []
            count = 0
            for good in goods:
                # 判断商品分类
                if count<4:
                    if type[0] == good.category_id:
                        goods_list.append(good)
                        count += 1
            # {'新鲜水果':[对象1，对象2,...],'猪牛羊肉':[对象1，对象2,...]}
            goods_dict[type[1]] = goods_list
        return render(request,'web/index.html',{'goods_dict':goods_dict,'types':types,'user':user})


# 注册页面
def register(request):
    if request.method == 'GET':
        return render(request,'web/register.html')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = make_password(form.cleaned_data.get('pwd'))
            User.objects.create(username=form.cleaned_data.get('user_name'),password=password,
                                email=form.cleaned_data.get('email'))
            return HttpResponseRedirect(reverse('front:index'))
        else:
            return render(request,'web/register.html',{'errors':form.errors})


# 商品详情展示页面
def show_goods_info(request,id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        types = GoodsCategory.CATEGORY_TYPE
        # 新品推荐实现
        # for type in types:
        #     if goods.category_id == type[0]:
        #         category_goods = Goods.objects.filter(category_id=type[0])
        category_goods = Goods.objects.filter(category_id=goods.category_id)
        categoods_list = []
        for good in category_goods:
            categoods_list.append(good)
        for categood in categoods_list:
            if categood.id == int(id):
                categoods_list.remove(categood)
        return render(request,'web/detail.html',{'goods':goods,'types':types,'categoods_list':categoods_list})


# 退出登录
def logout(request):
    if request.method == 'GET':
        del request.session['user_id']
        del request.session['goods']
        return HttpResponseRedirect(reverse('front:login'))


# 用户个人中心
def user_center_info(request):
    if request.method == 'GET':
        return render(request,'web/user_center_info.html',{'user':request.user})


# 购物车页面
def cart(request):
    if request.method == 'GET':
        # 如果没有登录。则从session中取商品的信息，登录还是从session取数据(保证数据库中的商品和session一致)
        session_goods = request.session.get('goods')
        if session_goods:
            goods_all = []
            for goods in session_goods:
                data = []
                cart_goods = Goods.objects.filter(pk=goods[0]).first()
                goods_number = goods[1]
                total_price = round((goods[1] * cart_goods.shop_price),2)
                goods_all.append([cart_goods,goods_number,total_price])
                # 获取商品对象,前台需要的商品信息，商品的个数，商品的总价
                # 后台返回结构[[goods_object,number,total_price]]
        else:
            goods_all = ''
        return render(request,'web/cart.html',{'goods':goods_all})


# 用户订单中心
def user_center_order(request):
    if request.method == 'GET':
        user = request.user
        return render(request,'web/user_center_order.html',{'users':user.useraddress_set.first()})



# 用户收货地址函数
def user_center_site(request):
    if request.method == 'GET':
        user = request.user
        return render(request,'web/user_center_site.html',{'users':user.useraddress_set.first()})
    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            UserAddress.objects.create(user=request.user,signer_name=form.cleaned_data.get('username'),
                                    address=form.cleaned_data.get('addr'),
                                    signer_mobile=form.cleaned_data.get('tel'),
                                    signer_postcode=form.cleaned_data.get('code')
                                    )
            return HttpResponseRedirect(reverse('front:user_center_site'))
        else:
            return render(request,'web/user_center_site.html',{'errors':form.errors})


# 加入购物车
def add_cart(request):
    if request.method == 'POST':
        # 需判断用户是否登录，登录则加入到数据库中，没有登录加入到session中
        # 如果登录则把session数据同步到数据库中(中间件同步)
        # 如果登录则加入到购物车的数据，存储到session中
        # session中存储数据：商品id,商品数量,商品的选择状态
        # [goods_id,goods_num,goods_status]
        # 1. 获取商品id和商品数量
        goods_id = int(request.POST.get('goods_id'))
        goods_num = int(request.POST.get('goods_num'))
        # 2. 组装存到session中的数据格式  1 代表选中状态
        goods_list = [goods_id,goods_num,1]

        if request.session.get('goods'):
            # 说明session中存储了加入到购物车的商品信息
            # 判断当前加入到购物车的数据，是否已经存在于session中
            # 如果存在，则修改session中该商品的数量，不存在则新增
            session_goods = request.session['goods']
            flag = 0
            for goods in session_goods:
                # 如果加入到购物车的数据已经存在于session中，则修改
                if goods[0] == goods_id:
                    goods[1] = int(goods[1]) + int(goods_num)
                    flag = 1
            # 如果不存在，添加
            if not flag:
                session_goods.append(goods_list)
            request.session['goods'] = session_goods
            goods_count = len(session_goods)
            return JsonResponse({'code':200,'msg':'请求成功','goods_count':goods_count})
        else:
            data = []
            data.append(goods_list)
            request.session['goods'] = data
        return HttpResponseRedirect(reverse('front:cart'))


# 结算
def place_older(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        carts = ShoppingCart.objects.filter(user_id=user_id,is_select=1).all()
        for cart in carts:
            cart.total_price = round((int(cart.nums)*cart.goods.shop_price),2)
        return render(request,'web/place_order.html',{'carts':carts})


def order(request):
    if request.method == 'POST':
        # 1.从购物车表中取出档当前系统用户is_select为1的商品信息
        user_id = request.session['user_id']
        carts = ShoppingCart.objects.filter(user_id=user_id,is_select=1).all()
        # 2.创建订单
        order_mount = 0
        for cart in carts:
            order_mount += int(cart.nums) * cart.goods.shop_price

        order = OrderInfo.objects.create(user_id=user_id,order_sn='',order_mount=order_mount)
        # 3.创建订单详情
        for cart in carts:
            OrderGoods.objects.create(order=order,goods=cart.goods,goods_nums=cart.nums)
        # 4.删除购物车中已经下单的商品信息
        carts.delete()
        return JsonResponse({'code':200,'msg':'请求成功'})


def f_price(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            carts = ShoppingCart.objects.filter(user_id=user_id)
            cart_data = {}
            cart_data['goods_price'] = [(cart.goods_id,
                                         cart.nums * cart.goods.shop_price)
                                        for cart in carts]
            all_price = 0
            for cart in carts:
                if cart.is_select:
                    all_price += cart.nums * cart.goods.shop_price
            cart_data['all_price'] = all_price
        else:
            session_goods = request.session.get('goods')
            cart_data = {}
            data_all = []
            all_price = 0
            for goods in session_goods:
                data = []
                data.append(goods[0])
                g = Goods.objects.get(pk=goods[0])
                data.append(int(goods[1]) * g.shop_price)
                if goods[2]:
                    all_price += int(goods[1]) * g.shop_price
            cart_data['goods_price'] = data_all
            cart_data['all_price'] = all_price
        return JsonResponse({'code': 200, 'cart_data': cart_data})


def cart_count(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if user_id:
            count = ShoppingCart.objects.filter(user_id=user_id).count()
        else:
            session_goods = request.session.get('goods')
            count = len(session_goods)
        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


def change_goods_num(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods_num = int(request.POST.get('goods_num'))
        is_select = int(request.POST.get('is_select'))

        user_id = request.session.get('user_id')

        session_goods = request.session.get('goods')
        if session_goods:
            for goods in session_goods:
                if goods_id == goods[0]:
                    goods[1] = goods_num
                    goods[2] = is_select
            request.session['goods'] = session_goods

        if user_id:
            ShoppingCart.objects.filter(user_id=user_id, goods_id=goods_id).update(nums=goods_num,
                                                                                   is_select=is_select)
        return JsonResponse({'code': 200, 'msg': '请求成功'})