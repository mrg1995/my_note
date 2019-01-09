import jieba
from django.shortcuts import render
import re
import random

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from api.models import User_info, Bt_test
from api.serializers import User_infoSerializer, UserSerializer, Bt_testSerializer
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework import viewsets, mixins
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django.http import Http404
from django.contrib import auth

import json
import jsonpath
from datetime import datetime
from django.db.models import Q
import time
from django.core.paginator import Paginator
from django.core.cache import cache
from api.task import send_Mail


# SessionAuthentication 会强行验证csrf
# 重写一个类继承SessionAuthentication, 并关闭csrf验证
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


# Create your views here.
# 注册用户
class UserList(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        # self.login_require(request)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 创建用户
    def post(self, request):
        data = request.data
        username = data.get('username')
        try:
            user = User.objects.get(username=username)
            if user:
                return Response({'error': '该用户名已被占用'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            pass
        password = data.get('password')
        if len(password) < 2 or len(password) > 12:
            return Response({'error': '密码长度2到12之间'}, status=status.HTTP_400_BAD_REQUEST)
        email = data.get('email')
        str1 = '(.+@.+\..+)'
        if not re.findall(str1, email):
            return Response({'error': '请输入正确的邮箱格式'}, status=status.HTTP_400_BAD_REQUEST)
        user1 = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_active=False,
        )
        user_info = User_info()
        user_info.user_id = user1.id
        user_info.save()
        # 生成token
        token = user_info.generate_token().decode()
        # celery发送邮件
        send_Mail.delay(token, [email])
        serializer = UserSerializer(user1)
        return Response({"info": '激活邮件已发送', "data": serializer.data}, status=status.HTTP_201_CREATED)


# 用户详情
class UserDetail(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist as e:
            raise Http404

    def get(self, request, pk):
        user = self.get_user(pk=pk)
        serializer1 = UserSerializer(user)
        user_info = user.user_info
        serializer2 = User_infoSerializer(user_info)
        dict1 = dict(list(serializer1.data.items()) + list(serializer2.data.items()))
        data = {"user_info": dict1}
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user1 = request.user
        if user1.id != int(pk):
            return Response({"info": '没有权限修改'}, status=status.HTTP_403_FORBIDDEN)
        user = self.get_user(pk=pk)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        user.set_password(password)
        user.username = username
        user.email = email
        user.save()
        serializer1 = UserSerializer(user)

        gender = data.get('gender')
        age = data.get('age')
        phone = data.get('phone')
        user_info = user.user_info
        user_info.gender = gender
        user_info.age = age
        user_info.phone = phone
        user_info.save()

        serializer2 = User_infoSerializer(user_info)
        dict1 = dict(list(serializer1.data.items()) + list(serializer2.data.items()))
        data = {"user_info": dict1}
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):

        user = self.get_user(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 登陆视图
class Login(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        pass

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active == False:
                return Response({"info": '请先激活'}, status=status.HTTP_403_FORBIDDEN)
            auth.login(request, user)
            return Response({"info": '登陆成功'}, status=status.HTTP_202_ACCEPTED)
        else:
            if not User.objects.get(username=username):
                return Response({"info": '用户名错误'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"info": '密码错误'}, status=status.HTTP_400_BAD_REQUEST)


# 登出
class Logout(APIView):
    def get(self, request):
        auth.logout(request)
        return Response({"info": '退出成功'}, status=status.HTTP_200_OK)


from rest_framework.exceptions import APIException


# 自定义异常处理
# 具体可看 https://www.jianshu.com/p/51b90b5453d2
class BadBadUnavailable(APIException):
    status_code = 400
    default_detail = '请输入正确的关键字'


class NiceNiceUnavailable(APIException):
    status_code = 400
    default_detail = '不能只输入1个数字或字母'


from rest_framework.pagination import PageNumberPagination

# 分页类
# 具体可看 https://www.jianshu.com/p/71b8749f6ae1
class AvSearchPagination(PageNumberPagination):
    page_size = 10
    # 控制 单页显示数量的
    page_size_query_param = 'size'
    page_query_param = 'p'
    # 单页显示最大数量  前提是要有page_size_query_param 参数
    max_page_size = 300


import django_filters

#  过滤类
# 具体可看 https://www.jianshu.com/p/7fe78a9e45ca
class AvFilter(django_filters.rest_framework.FilterSet):
    # lookup_expr 是查找方式 , name 是 数据表中的字段名
    kw = django_filters.CharFilter(name='av_name', lookup_expr='icontains')

    class Meta:
        model = Bt_test
        # 这个kw 是在 url中查询的显示字段
        fields = ['kw']

# bt 搜索视图
# CacheResponseMixin 调用了 drf-extension 的缓存插件
# 具体方法可看 https://www.jianshu.com/p/f0c78a81348c
class BtsearchViewset(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Bt_test.objects.all()
    serializer_class = Bt_testSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = AvSearchPagination
    # 定义需要使用过滤器的字段
    filter_class = AvFilter

    # 因为我需要在查询时对关键字做一些过滤
    # 因此重写get_queryset的方法
    def get_queryset(self):
        # request.query_params 是 request.GET在restframework中的写法
        av_name = self.request.query_params.get('kw', None)
        # 当查询时 ,不允许没有关键字,以及只输入1个数字或字母
        if self.action == 'list':
            if not av_name:
                raise BadBadUnavailable
            if len(av_name) == 1 and re.findall('[a-zA-Z0-9]', av_name):
                raise NiceNiceUnavailable
        return Bt_test.objects.all()


# 搜索视图
class Main(APIView):
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        data = request.GET
        str1 = data.get('kw')
        page = data.get('pg')
        if not str1:
            return render(request, 'shouye.html')
        # 判断是否有传入页码
        if not page:
            page = 1
        # 判断 页码 是否正确
        if not re.findall('[0-9]+', str(page)):
            return Response({'info': '错误的页码'}, status=status.HTTP_400_BAD_REQUEST)
        # 判断 关键字 是否正确
        if len(str1) == 1 and re.findall('[a-zA-Z0-9]', str1):
            return Response({"info": '不能只输入一个字母或数字'}, status=status.HTTP_400_BAD_REQUEST)
        # 进行关键字分词查询
        search = jieba.cut_for_search(str1)  # 按搜索引擎方式切割
        if not request.user.is_authenticated():
            nice = ('结衣', '波多', 'porn')
        else:
            nice = ('富强', '民主', '和谐', '自强')
        # 对查询到的结果缓存  提高查询效率
        num = 1
        time2 = time.time()
        bts = Bt_test.objects.filter(pk=300)
        for i in search:
            if num > 4:
                break
            if i in nice:
                continue
            bt = cache.get(i)
            if not bt:
                bt = Bt_test.objects.filter(Q(av_name__icontains=i))
                cache.set(i, bt, 86300)
            bts |= bt
            num += 1
        print('获取数据时间{}'.format(time.time() - time2))
        # 进行分页
        time1 = time.time()
        paginator = Paginator(bts, 6)
        print('分页时间{}'.format(time.time() - time1))
        # 如果传入的页码大于分页  则页码为分页最大值
        if int(page) > paginator.num_pages:
            page = paginator.num_pages
        btss = paginator.page(page)
        # bts = Bt_test.objects.filter(*Qs)
        serializer = Bt_testSerializer(btss, many=True)

        data = {"page": btss, "data": btss.object_list, "kw": str1, 'post_list': bts}
        return Response({"page": paginator.num_pages, "data": serializer.data}, status=status.HTTP_200_OK)
        # return render(request,'sousuoyemian.html',context=data)

    def post(self, request):
        fileName = open('bt1.json', 'rb')
        str = fileName.readlines()[0]
        str1 = str.decode('utf-8')
        data = '{"data":[' + str1[:(len(str1) - 1)] + ']}'
        jsonobj = json.loads(data)
        btList = jsonpath.jsonpath(jsonobj, '$.data')[0]
        time.time()

        for bt in btList:
            # print(bt,type(bt))
            try:
                bt1 = Bt_test()
                bt1.av_name = bt['av_name']
                bt1.magent = bt['margent']
                bt1.hash_info = bt['hash_info']
                bt1.time_info = datetime.strptime(bt['time_info'], '%Y-%m-%d')
                bt1.size_info = bt['size_info']
                bt1.save()
            except:
                pass
        fileName.close()
        print(time.clock())
        return Response({"info": '插入完成'}, status=status.HTTP_201_CREATED)


# 种子详情
class Detail(APIView):
    # 通过 id 来查找种子
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, pk):
        serializer = cache.get(pk)
        if not serializer:
            bt = Bt_test.objects.filter(pk=pk)
            if not bt:
                return Response({'info': '不要搞事情'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = Bt_testSerializer(bt[0])
            cache.set(pk, serializer, 86300)
        bt2 = Bt_test.objects.filter(pk=pk)
        if not bt2:
            return Http404
        bt3 = Bt_test.objects.filter(pk=int(pk) - 1)
        bt4 = Bt_test.objects.filter(pk=int(pk) + 1)
        data = {'data': bt2[0], 'data1': bt3[0], 'data2': bt4[0]}

        # return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return render(request, 'xiangqing.html', context=data)

    def post(self, request, pk):
        user = request.user
        if not user.is_authenticated():
            return Response({"info": '未登录'}, status=status.HTTP_403_FORBIDDEN)
        bt = Bt_test.objects.get(pk=pk)
        if user.favorite.filter(id=pk):
            bt.favorite.remove(user)
        else:
            bt.favorite.add(user)
        return Response({'info': '操作成功'}, status=status.HTTP_201_CREATED)


class Check(APIView):
    def get(self, request, token):
        if User_info.check_token(token):
            return Response({'info': '激活成功'}, status=status.HTTP_200_OK)
        else:
            return Response({'info': '激活失败'}, status=status.HTTP_200_OK)


class UserFav(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        btLs = user.favorite.all()
        serializer = Bt_testSerializer(btLs, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
