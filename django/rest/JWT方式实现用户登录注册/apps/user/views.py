from random import choice
from django.shortcuts import HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import permissions, status
from .serializers import UserDetailSerializer, UserRegisterSerializer, SmsSerializer
from .models import VerifyCode

User = get_user_model()

# 重写 用户的检测 这样可以通过 用户名 或者 手机号登陆
# 具体看 https://www.jianshu.com/p/a3c6bc69a804
class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    验证码
    create:
        获得验证码
    '''
    serializer_class = SmsSerializer

    # 生成4位手机验证码
    def generate_code(self):
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 序列化类 检查过的对象放在validated_data中
        mobile = serializer.validated_data['mobile']
        code = self.generate_code()
        # 将手机号与验证码存入VerifyCode表
        code_record = VerifyCode(code=code, mobile=mobile)
        code_record.save()
        return Response({'res': 1, 'data': {'code': code}})


# 视图解释 看 https://www.jianshu.com/p/3cec36add17d
# 一般 继承 viewsets.GenericViewSet  和一些 mixins类 来构成视图
# 如果要重写一些方法 如本视图中的  create 方法 就是 重写的 CreateModelMixin 中的方法
class UserViewSets(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    '''
    create:
        注册新用户
    '''
    queryset = User.objects.all()
    # 认证方式为JSONWebTokenAuthentication方式
    # 具体可看 http://getblimp.github.io/django-rest-framework-jwt/
    authentication_classes = (JSONWebTokenAuthentication,)

    #   viewsets视图类中多了个 action 属性 (请求的方式) list retrieve 是一般的get请求   create 就是post请求
    # restframework中只有viewsets视图类中有这个action属性, 这样又能高定制化也能快速的写视图
    # 自定义不同请求下的 序列化类
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegisterSerializer
        return UserDetailSerializer
    # 自定义不同请求下的 权限
    def get_permissions(self):
        if self.action == 'retreve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    # 自定义 create 方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        # 手动生成 JWT token 的方式
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.nick_name if user.nick_name else user.username
        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # create()方法会调用  perform_create()方法 具体可以看 mixins.CreateModelMixin 的源码
    def perform_create(self, serializer):
        return serializer.save()


    # 用户不知道自己的id是多少,可以通过这种方法,不管id输入多少,都返回自己的信息
    def get_object(self):
        return self.request.user
