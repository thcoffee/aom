from django.conf.urls import url
from django.conf.urls import  include, url  
from django.contrib.auth import views as views1
from . import views
urlpatterns = [
url(r'^test/$', views.test, name='test'),
url(r'^test1/$', views.test1, name='test1'),
url(r'^installsoftlist/$', views.installsoftList, name='installsoftlist'),
url(r'^installjdkadd/$', views.installjdkAdd, name='installjdkadd'),
url(r'^jdkcommit/$', views.jdkcommit, name='jdkcommit'),
url(r'^installsoftinfo/$', views.installsoftinfo, name='installsoftinfo'),
url(r'^logout/$', views1.LogoutView.as_view(), name='logout')
]