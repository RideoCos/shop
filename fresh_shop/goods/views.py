
from django.shortcuts import render
from goods.models import GoodsCategory,Goods
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from goods.forms import GoodsForm
from fresh_shop.settings import PAGE_NUMBER

def goods_category_list(request):
    if request.method == 'GET':
        categorys = GoodsCategory.objects.all()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request,'back/goods_category_list.html',{'categorys':categorys,'types':types})


def good_category_detail(request,id):
    if request.method == 'GET':
        category = GoodsCategory.objects.filter(pk=id).first()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request,'back/goods_category_detail.html',{'category':category,'types':types})
    if request.method == 'POST':
        img = request.FILES.get('category_front_image')
        if img:
            category = GoodsCategory.objects.filter(pk=id).first()
            category.category_front_image = img
            category.save()
            return HttpResponseRedirect(reverse('goods:goods_category_list'))
        else:
            error = '选择图片'
            return render(request,'goods_category_detail.html',{'error':error})


def goods_list(request):
    if request.method == 'GET':
        # TODO:查询所有商品信息，并在goods_list.html页面解析
        goods = Goods.objects.all()
        types = GoodsCategory.CATEGORY_TYPE
        try:
            page = request.GET.get('page', 1)
        except Exception as e:
            # 如果地址的页码输入为非数字，将页面设置为1 ?page=asd
            page = 1
        # 分页，每一页三条数据
        paginator = Paginator(goods, PAGE_NUMBER)
        # 获取某一页数据
        goods = paginator.page(page)
        return render(request,'back/goods_list.html',{'goods':goods,'types':types})


def goods_add(request):
    if request.method == 'GET':
        types = GoodsCategory.CATEGORY_TYPE
        return render(request,'back/goods_detail.html',{'types':types})
    if request.method == 'POST':
        # TODO:验证商品信息的完整性，数据的保存
        # 使用表单验证
        form = GoodsForm(request.POST,request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            Goods.objects.create(**data)
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            # 验证失败
            return render(request,'back/goods_detail.html',{'errors':form.errors})


def goods_del(request,id):
    if request.method == 'POST':
        # ajax删除商品 JsonResponse
        Goods.objects.filter(pk=id).delete()
        return JsonResponse({'code':200,'msg':'请求成功'})


def goods_edit(request,id):
    if request.method == 'GET':
        # 要编辑的商品对象
        goods = Goods.objects.filter(pk=id).first()
        types = GoodsCategory.CATEGORY_TYPE
        return render(request,'back/goods_detail.html',{'goods':goods,'types':types})
    if request.method == 'POST':
        form = GoodsForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            # 把图片从data中剔除
            # 更新时没有选择图片，图片字段为None，有图片字段为图片名字，没有路径前缀
            img = data.pop('goods_front_image')
            if img:
                goods = Goods.objects.filter(pk=id).first()
                goods.goods_front_image = img
                goods.save()
            # 更新除了图片的其他信息
            Goods.objects.filter(pk=id).update(**data)
            return HttpResponseRedirect(reverse('goods:goods_list'))
        else:
            # 验证失败
            goods = Goods.objects.filter(pk=id).first()
            types = GoodsCategory.CATEGORY_TYPE
            return render(request, 'back/goods_detail.html', {'errors': form.errors,'types':types,'goods':goods})


def goods_desc(request,id):
    if request.method == 'GET':
        # 如果有内容，返回商品对象，刷新内容
        return render(request,'back/goods_desc.html')
    if request.method == 'POST':
        # 获取编辑器的内容
        content = request.POST.get('content')
        # 获取修改商品对象
        goods = Goods.objects.filter(pk=id).first()
        goods.goods_desc = content
        goods.save()
        return HttpResponseRedirect(reverse('goods:goods_list'))


def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return HttpResponseRedirect(reverse('back:login'))
