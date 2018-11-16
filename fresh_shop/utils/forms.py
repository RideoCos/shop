from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=10,min_length=2,required=True,
                               error_messages={
                                   'required':'必填',
                                   'max_length':'用户名过长',
                                   'min_length':'用户名过短'
                               })
    password = forms.CharField(required=True,
                                error_messages={
                                   'required': '必填',
                               })

    def clean(self):
        # 使用django自带的User模块进行验证
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if not user:
            raise forms.ValidationError({'username':'该账号没有注册，请去注册'})

        return self.cleaned_data
