import datetime
import hashlib

from django.shortcuts import render, redirect
from django.utils import timezone

from login import models, forms

from django.conf import settings


def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自积木编程网的注册确认邮件'

    text_content = '''感谢注册积木编程网，这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000/user/', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def hash_code(s, salt='shopping'):  # 加点盐
    h = hashlib.sha3_256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    # 如果取is_login的值不存在，则返回None, not后变True 也就返回登录页面
    if not request.session.get('is_login', None):
        return redirect('user_login')
    return render(request, 'login/index.html')
    # context = {
    #     'title': '会员登录'
    # }
    # return render(request, 'login/index.html', context)


# def login(request):
#     pass
#     if request.method == 'POST':
#         # user_form = request.POST
#         username_f = request.POST.get('username')
#         password = request.POST.get('password')
#         message = '请先填写正确的账户和密码~！'
#
#         if username_f and password:
#             try:
#                 # 这里仅仅验证账户是否存在，密码是否正确，更多的其它验证可增加..
#                 user = models.User.objects.get(username=username_f)
#             except:
#                 message = '账户不存在'
#                 return render(request, 'login/index.html', {'message': message})
#             if user.password == password:
#                 return redirect('/admin/')
#             else:
#                 message = '账户密码错误'
#                 return render(request, 'login/index.html', {'message': message})
#         else:
#             return render(request, 'login/index.html', {'message': message})
#
#         # return render(request, 'login/login.html', locals())
#     else:
#         message = '来源不正确'
#         return render(request, 'login/index.html', {'message': message})


def register(request):
    if request.session.get('is_login', None):
        return redirect('user_index')

    if request.method == 'POST':
        reg_form = forms.RegisterForm(request.POST)
        message = '请检查填写的内容！'

        if reg_form.is_valid():
            username_f = reg_form.cleaned_data.get('username')
            email_f = reg_form.cleaned_data.get('email')
            password1 = reg_form.cleaned_data.get('password1')
            password2 = reg_form.cleaned_data.get('password2')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username_f)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_name_user = models.User.objects.filter(email=email_f)
                if same_name_user:
                    message = '邮箱已经存在'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.username = username_f
                new_user.email = email_f
                new_user.password = hash_code(password1)
                new_user.save()  # 保存提交用户信息

                # 增加邮件地址验证 把新注册用户制作出code验证码
                code = make_confirm_string(new_user)
                send_email(email_f, code)

                message = '请前往邮箱进行确认！'
                return render(request, 'login/confirm.html', locals())

        else:
            return render(request, 'login/register.html', locals())

    reg_form = forms.RegisterForm(request.POST)
    return render(request, 'login/register.html', locals())


def login(request):
    # 检测is_login的值是否存在，存在则为True,不存在则返回None,存在返回用户页面
    if request.session.get('is_login', None):
        return redirect('user_index')
    # 检测用户登录是否post提交
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'

        if login_form.is_valid():
            username_f = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(username=username_f)
            except:
                message = '您输入的账户不存在'
                return render(request, 'login/login.html', locals())
            # 判断邮件是否验证
            if not user.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                return redirect('user_index')
            else:
                message = '您输入的密码错误'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("user_login")
    # request.session.clear()
    # 或者使用下面的方法
    del request.session['is_login']
    del request.session['user_id']
    del request.session['user_name']
    return redirect("user_login")


# 邮件地址验证方法
def make_confirm_string(user):
    now = str(datetime.datetime.now())
    code = hash_code(user.username, now)
    #   把传入的user生产出code写入数据库，同时方法返回code
    models.ConfirmString.objects.create(code=code, user=user)
    return code


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    # now = datetime.datetime.now()
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
