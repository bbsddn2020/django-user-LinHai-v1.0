# 首先引入django的表单模型
from captcha.fields import CaptchaField
from django import forms


# 创建UserForm继承django的表单模型


class UserForm(forms.Form):
    required_css_class = 'form-group'
    # 创建表单模型
    username = forms.CharField(
        label='用户名', max_length=128, widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': "输入用户名", 'autofocus': ''
        })
    )
    password = forms.CharField(
        label='密码', max_length=128, widget=forms.PasswordInput({
            'class': 'form-control', 'placeholder': "输入登录密码"
        })
    )
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名', max_length=128, widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "输入用户名",
                'autofocus': ''
            }
        )
    )
    email = forms.CharField(
        label='邮箱', max_length=128, widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        label='密码', max_length=128, widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label='重复密码', max_length=128, widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    captcha = CaptchaField(label='验证码')
