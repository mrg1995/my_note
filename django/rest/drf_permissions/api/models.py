from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.

class UserProfile(AbstractUser):
    '''
    用户
    '''
    nick_name = models.CharField(max_length=20,null=True,blank=True)
    permissions = models.IntegerField(default=3,blank=True,null=True)


User = get_user_model()

class Post(models.Model):
    '''
    文章
    '''
    user = models.ForeignKey(to=User)
    post = models.CharField(max_length=100,blank=True,null=True)
    modify_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)







