from django.db import models
from django.contrib.auth.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings


# Create your models here.


class User_info(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(blank=True, null=True)
    gender = models.BooleanField(default=False)
    phone = models.CharField(max_length=16, blank=True, null=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_info'
        ordering = ['id']

    # 生成token的方法
    def generate_token(self):
        # 调用 TimedJSONWebSignatureSerializer方法 参数为自己设置的SECRET_KEY
        s = Serializer(settings.SECRET_KEY)
        print(self.user_id)
        return s.dumps({'id': self.user_id})

    # 检测token的方法
    @staticmethod
    # 传入获取的token
    def check_token(token):
        s = Serializer(settings.SECRET_KEY)
        # 从当前的token中拿出字典
        try:
            id = s.loads(token)['id']
        except:
            # 如果token有问题 返回false
            return False
        # 根据用户id取出对应用户的对象
        u = User.objects.filter(pk=id)
        # 判断 当前u对象是否存在
        if not u:
            return False
        # 判断当期用户的激活状态 如果没有激活 则激活
        if not u[0].is_active:
            u[0].is_active = True
            u[0].save()
        return True


class Bt_test(models.Model):
    av_name = models.CharField(max_length=200)
    magent = models.CharField(max_length=200)
    hash_info = models.CharField(max_length=100)
    time_info = models.DateTimeField(help_text='创建时间')
    size_info = models.CharField(max_length=50, help_text='大小')
    favorite = models.ManyToManyField(User, help_text='收藏该种子的用户', related_name='favorite')

    def __str__(self):
        return self.av_name

    class Meta:
        db_table = 'bts'
