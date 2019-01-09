from django.conf.urls import url,include
from .views import User_login,User_logout






urlpatterns = [
    url(r'^user/login/', User_login.as_view()),
    url(r'^user/logout/', User_logout.as_view()),
]