from django.conf.urls import url
from django.conf.urls import  include, url  
from django.contrib.auth import views as views1
from . import views
urlpatterns = [
url(r'^test/$', views.test, name='test'),
url(r'^test1/$', views.test1, name='test1'),
url(r'^installsoftwarelist/$', views.installsoftwareList, name='installsoftwarelist'),
url(r'^installsoftwareadd/$', views.installsoftwareAdd, name='installsoftwareadd'),
url(r'^jdkcommit/$', views.jdkcommit, name='jdkcommit'),
url(r'^installsoftwareinfo/$', views.installsoftwareinfo, name='installsoftwareinfo'),
url(r'^logout/$', views1.LogoutView.as_view(), name='logout')
]