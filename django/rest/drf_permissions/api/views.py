import jwt
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication
from api.models import Post
from .serializer import  UserRegisterSerializer,UserDetailSerializer,PostSerialzier
from .permissions import IsSuperUserOrOwnerDelete, IsOwnerUpdate

# Create your views here.
User = get_user_model()
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return

class UsersViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication,)
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        if self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer
    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []
    def get_object(self):
        return self.request.user

class User_login(APIView):
    def post(self,request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        if not username:
            return Response({'info': '请输入姓名'})
        if not password:
            return Response({'info': '请输入密码'})
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active == False:
                return Response({'info': '请先激活'}, status=status.HTTP_400_BAD_REQUEST)
            auth.login(request, user)
            return Response({"info": "登陆成功"}, status=status.HTTP_200_OK)
        else:
            return Response({'info': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)

class User_logout(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    def get(self, request):
        auth.logout(request)
        return Response({'info': '退出成功'})

class PostsViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = Post.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = PostSerialzier
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsSuperUserOrOwnerDelete(),]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'update':
            return [IsOwnerUpdate(),]
        return []




