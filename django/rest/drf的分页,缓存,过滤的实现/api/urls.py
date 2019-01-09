from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'bts',views.BtsearchViewset,base_name='bts')


urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^logout/$', views.Logout.as_view()),
    url(r'^main/', views.Main.as_view(),name='main'),
    url(r'^detail/(?P<pk>\d+)/$', views.Detail.as_view(),name='detail'),
    url(r'^check/(?P<token>.+)/$', views.Check.as_view()),
    url(r'^userfav/', views.UserFav.as_view()),
    url(r'^search/',include(router.urls))

]
