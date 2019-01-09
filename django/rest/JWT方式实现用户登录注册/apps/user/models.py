from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# Create your models here.

# 继承AbstractUser类  重写auth表
# 具体看笔记 https://www.jianshu.com/p/68c756435277
class UserProfile(AbstractUser):
    gender_type = (
        (0,'女'),
        (1,'男')
    )
    nick_name = models.CharField(max_length=30,null=True,blank=True)
    gender = models.IntegerField(choices=gender_type,null=True,blank=True)
    mobile = models.CharField(max_length=11,null=True,blank=True)
    isDelete = models.BooleanField(default=False)
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

User = get_user_model()

class VerifyCode(models.Model):
    code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=11)
    add_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code






