from django import forms
from goods.models import GoodsCategory

class GoodsForm(forms.Form):
    name = forms.CharField(required=True,max_length=50,error_messages={'required':'商品名称必填','max_length':'商品名称过长'})
    goods_sn = forms.CharField(required=True,error_messages={'required':'商品货号必填' })
    category = forms.CharField(required=True,error_messages={'required':'商品分类必填' })
    goods_nums = forms.CharField(required=True,error_messages={'required':'商品库存必填'})
    market_price = forms.CharField(required=True,error_messages={'required':'商品市场价格必填'})
    shop_price = forms.CharField(required=True,error_messages={'required':'本店价格必填'})
    goods_brief = forms.CharField(required=True,error_messages={'required':'商品说明必填'})
    goods_front_image = forms.ImageField(required=False,error_messages={'required':'商品首图必填'})

    # 检验分类
    def clean_category(self):
        id = self.cleaned_data.get('category')
        category = GoodsCategory.objects.filter(pk=id).first()
        return category




