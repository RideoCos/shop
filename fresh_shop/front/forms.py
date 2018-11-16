from django import forms
from goods.models import User
import re

class UserRegisterForm(forms.Form):
    user_name = forms.CharField(required=True,max_length=20,min_length=5,error_messages={'required':'用户名必填',
                                                                                         'max_length':'用户名不能超过20位',
                                                                                         'min_length':'用户名不能短于5位'})
    pwd = forms.CharField(required=True,max_length=20,min_length=8,error_messages={'required':'密码必填',
                                                                                   'max_length':'密码超过20位',
                                                                                   'min_length':'密码最短8位'})
    cpwd = forms.CharField(required=True,max_length=20,min_length=8,error_messages={'required':'密码必填',
                                                                                    'max_length': '密码超过20位',
                                                                                    'min_length': '密码最短8位'})
    email = forms.CharField(required=True,error_messages={'required':'邮箱必填'})
    allow = forms.CharField(required=True,error_messages={'required':'是否同意协议'})

    def clean(self):
        name = self.cleaned_data.get('user_name')
        user = User.objects.filter(username=name).first()
        if user:
            raise forms.ValidationError({'user_name': '该账户已注册'})
        if self.cleaned_data.get('pwd') != self.cleaned_data.get('cpwd'):
            raise forms.ValidationError({'pwd':'密码不一致'})
        return self.cleaned_data



class UserLoginForm(forms.Form):
    username = forms.CharField(required=True,max_length=10,min_length=5,error_messages={'required':'请填写用户名',
                                                                                        'max_length':'用户名不能超过10位',
                                                                                        'min_length':'用户名不能少于5位'})
    pwd = forms.CharField(required=True,max_length=20,min_length=8,error_messages={'required':'请填写用户名',
                                                                                   'max_length':'密码长度不能超过20位',
                                                                                   'min_length':'密码长度不能小于8位'})

    def clean(self):
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if not user:
            raise forms.ValidationError({'username':'该用户尚未注册，请前往注册'})
        return self.cleaned_data


class AddressForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,min_length=1,error_messages={'required':'收件人必填',
                                                                                        'max_length':'用户名过长',
                                                                                        'min_length':'用户名至少两个字'})
    addr = forms.CharField(required=True,min_length=10,max_length=50,error_messages={'required':'收获地址必填',
                                                                                    'min_length':'地址长度不能小于10位',
                                                                                    'max_length':'地址过长'})
    code = forms.CharField(required=False,error_messages={'required':'必须是6位邮编'})
    tel = forms.CharField(required=True,error_messages={'required':'手机号必填'})

    def clean(self):
        phone = self.cleaned_data.get('tel')
        postcode = self.cleaned_data.get('code')
        if not all([postcode,phone]):
            phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
            res = re.fullmatch(phone_pat, phone)
            if not res:
                raise forms.ValidationError({'tel':"手机号格式错误"})
        return self.cleaned_data

