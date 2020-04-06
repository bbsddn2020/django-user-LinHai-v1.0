import os
from django.core.mail import send_mail


os.environ['DJANGO_SETTINGS_MODULE'] = 'django3vue.settings'

if __name__ == '__main__':

    send_mail(
        '我和你能联通吗？',
        '欢迎访问www.liujiangblog.com，这里是刘江的博客和教程站点，本站专注于Python、Django和机器学习技术的分享！',
        'liulin160@163.com',
        ['177060606@qq.com'],
    )