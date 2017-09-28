from django.conf.urls import url
from django.conf.urls import  include, url  
from django.contrib.auth import views as views1
from . import views
urlpatterns = [
url(r'^test/$', views.test, name='test'),
url(r'^test1/$', views.test1, name='test1'),
#安装软件列表
url(r'^installsoftlist/$', views.installsoftList, name='installsoftlist'),
#安装jdk表单
url(r'^installjdkadd/$', views.installjdkAdd, name='installjdkadd'),
#jdk提交程序
url(r'^jdkcommit/$', views.jdkcommit, name='jdkcommit'),
#安装jdk表单
url(r'^installnginxadd/$', views.installnginxAdd, name='installnginxadd'),
#jdk提交程序
url(r'^nginxcommit/$', views.nginxcommit, name='nginxcommit'),

#安装jdk表单
url(r'^installtomcatadd/$', views.installtomcatAdd, name='installtomcatadd'),
#jdk提交程序
url(r'^tomcatcommit/$', views.tomcatcommit, name='tomcatcommit'),

#安装软件相信信息
url(r'^installsoftinfo/$', views.installsoftinfo, name='installsoftinfo'),
#post接口
url(r'^postData/$', views.postData, name='postData'),
#注销
url(r'^logout/$', views1.LogoutView.as_view(), name='logout')
]