"""project_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import refresh_jwt_token,obtain_jwt_token,verify_jwt_token

from user.views import UserViewSets, SmsCodeViewset

router = DefaultRouter()
router.register(r'codes', SmsCodeViewset, base_name='codes')
router.register(r'users', UserViewSets, base_name='users')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'docs/', include_docs_urls(title="鲍勃")),
    # 获得token
    url(r'^api-token-auth/', obtain_jwt_token),
    # 将未过期的token 刷新 重置过期时间
    url(r'^api-token-refresh/', refresh_jwt_token),
    # 验证令牌
    url(r'^api-token-verify/', verify_jwt_token),
]


