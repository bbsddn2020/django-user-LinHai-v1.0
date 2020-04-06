from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="用户名")
    email = models.CharField(max_length=150, unique=True, verbose_name="邮件")
    password = models.CharField(max_length=150, verbose_name="密码")
    has_confirmed = models.BooleanField(default=False, verbose_name="邮件激活")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "注册用户"


# 创建验证码模型
class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":   " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "确认码"
