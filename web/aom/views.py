from django.shortcuts import render
from django.db import connections,transaction
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import pymysql
#导入数据库操作模块
from . import db

# Create your views here.

#分页
def _my_pagination(request, queryset, display_amount=10, after_range_num = 5,bevor_range_num = 4):
    #按参数分页
    paginator = Paginator(queryset, display_amount)
    try:
        #得到request中的page参数
        page =int(request.GET.get('page'))      
    except:
        #默认为1
        page = 1
    #页码超出范围指向1    
    if page <1 or page >  paginator.num_pages:
        page=1        
    try:
        #尝试获得分页列表
        objects = paginator.page(page)
    #如果页数不存在
    except EmptyPage:
        #获得最后一页
        objects = paginator.page(paginator.num_pages)
    #如果不是一个整数
    except:
        #获得第一页
        objects = paginator.page(1)
    #根据参数配置导航显示范围
    if page >=after_range_num and paginator.num_pages-page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    elif page >= after_range_num and page >paginator.num_pages-after_range_num:
        page_range = paginator.page_range[-(after_range_num+bevor_range_num):]
    else:
        page_range = paginator.page_range[0:bevor_range_num+bevor_range_num+1]
    return objects,page_range

#初始化
def _initPage(request):
    data={}
    data['userid']=str(request.user)
    return(data)
    
@login_required(login_url="/admin/login/")      
def test(request):
    data=_initPage(request)
    sql='select * from adc_deploy order by 1 limit 0,121'
    dbcon=db.opMysqlObj(**{'dbname':'zsj'})
    objects, page_range = _my_pagination(request, dbcon.getData(**{'sql':sql}))
    dbcon.close()
    objects_head=['字段1','字段2','字段3','字段4','字段5','字段6']
    data['objects']=objects
    data['page_range']=page_range
    data['objects_head']=objects_head
    return render(request, 'aom/test.html',data)

#安装软件列表    
@login_required(login_url="/admin/login/")   
def installsoftList(request):
    data=_initPage(request)
    sql="SELECT a.taskid,a.taskdate,f.`softname`,f.`softversion`,c.`username`,d.`taskstatusname` FROM (SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_before WHERE tasktype='installsoftware' UNION ALL  SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_after WHERE tasktype='installsoftware')  a LEFT JOIN aom_task_type b ON a.tasktype=b.tasktypeid LEFT JOIN auth_user c ON a.userid=c.`id` LEFT JOIN aom_task_status d ON a.taskstatus=d.`taskstatusid` LEFT JOIN aom_task_soft e ON a.taskid=e.`taskid` LEFT JOIN aom_softtype f ON  e.`softtypeid`=f.`softtypeid` ORDER BY a.taskid DESC"
    dbcon=db.opMysqlObj(**{'dbname':'default'})
    objects, page_range = _my_pagination(request, dbcon.getData(**{'sql':sql}))
    dbcon.close()
    objects_head=['任务ID','任务日期','软件名','软件版本','用户','状态']
    data['objects']=objects
    data['page_range']=page_range
    data['objects_head']=objects_head
    return render(request, 'aom/installsoftlist.html',data)

#安装jdk表单
def installjdkAdd(request):
    data=_initPage(request)
    sql="SELECT softtypeid,softname,softversion FROM aom_softtype where softname='jdk' ORDER BY 2,3;"
    dbcon=db.opMysqlObj(**{'dbname':'default'})
    data['softinfo']= dbcon.getData(**{'sql':sql})
    data['nodes']= dbcon.getNodes()
    dbcon.close()
    return render(request, 'aom/installjdkadd.html',data) 

#接收安装jdk表单提交
def jdkcommit(request):
    if request.method != "POST":
        return HttpResponse("参数错误")
    sql="SELECT softpath,softfiles FROM aom_softtype where softTYPEID="+request.POST.get('softversion',1)
    d=db.opMysqlObj(**{'dbname':'default'})
    #print(request.POST.getlist('nodeselect'))
    localpathfiles=d.getData(sql=sql)
    data={'task':'installsoftware',
          'localpath':localpathfiles[0][0],
          'localfiles':localpathfiles[0][1],
          'remotepath':request.POST.get('remotepath',''),
          'name':'jdk','node':request.POST.getlist('nodeselect')}
    
    d.putData(sql="INSERT INTO aom_task_before (taskdate,tasktype,userid,taskstatus,taskcontent) VALUES (NOW(),'installsoftware',1,1,\"%s\")" %(str(data)))
    d.putData(sql="insert into aom_task_soft (taskid,softTYPEID)values (%s,%s)"%(d.getLaseID(),request.POST.get('softversion',1)))
    d.commit()
    d.close()
    return HttpResponseRedirect("/aom/installsoftlist/")  

#安装jdk表单
def installnginxAdd(request):
    data=_initPage(request)
    sql="SELECT softtypeid,softname,softversion FROM aom_softtype where softname='nginx' ORDER BY 2,3;"
    dbcon=db.opMysqlObj(**{'dbname':'default'})
    data['softinfo']= dbcon.getData(**{'sql':sql})
    data['nodes']= dbcon.getNodes()
    dbcon.close()
    return render(request, 'aom/installnginxadd.html',data) 

#接收安装jdk表单提交
def nginxcommit(request):
    if request.method != "POST":
        return HttpResponse("参数错误")
    sql="SELECT softpath,softfiles FROM aom_softtype where softTYPEID="+request.POST.get('softversion',1)
    d=db.opMysqlObj(**{'dbname':'default'})
    #print(request.POST.getlist('nodeselect'))
    localpathfiles=d.getData(sql=sql)
    data={'task':'installsoftware',
          'localpath':localpathfiles[0][0],
          'localfiles':localpathfiles[0][1],
          'remotepath':request.POST.get('remotepath',''),
          'name':'nginx','node':request.POST.getlist('nodeselect')}
    print(str(data))
    d.putData(sql="INSERT INTO aom_task_before (taskdate,tasktype,userid,taskstatus,taskcontent) VALUES (NOW(),'installsoftware',1,1,\"%s\")" %(str(data)))
    d.putData(sql="insert into aom_task_soft (taskid,softTYPEID)values (%s,%s)"%(d.getLaseID(),request.POST.get('softversion',1)))
    d.commit()
    d.close()
    return HttpResponseRedirect("/aom/installsoftlist/")      


#安装jdk表单
def installtomcatAdd(request):
    data=_initPage(request)
    sql="SELECT softtypeid,softname,softversion FROM aom_softtype where softname='tomcat' ORDER BY 2,3;"
    dbcon=db.opMysqlObj(**{'dbname':'default'})
    data['softinfo']= dbcon.getData(**{'sql':sql})
    data['nodes']= dbcon.getNodes()
    dbcon.close()
    return render(request, 'aom/installtomcatadd.html',data) 

#接收安装jdk表单提交
def tomcatcommit(request):
    if request.method != "POST":
        return HttpResponse("参数错误")
    sql="SELECT softpath,softfiles FROM aom_softtype where softTYPEID="+request.POST.get('softversion',1)
    d=db.opMysqlObj(**{'dbname':'default'})
    #print(request.POST.getlist('nodeselect'))
    localpathfiles=d.getData(sql=sql)
    data={'task':'installsoftware',
          'localpath':localpathfiles[0][0],
          'localfiles':localpathfiles[0][1],
          'remotepath':request.POST.get('remotepath',''),
          'name':'tomcat',
          'httpport':request.POST.get('httpport',''),
          'shutdownport':request.POST.get('shutdownport',''),
          'ajpport':request.POST.get('ajpport',''),
          'basedir':request.POST.get('basedir',''),
          'docbase':request.POST.get('docbase',''),
          'appbase':request.POST.get('appbase',''),
          'javahome':request.POST.get('javahome',''),
          'javaopt':request.POST.get('javaopt',''),
          'node':request.POST.getlist('nodeselect')}
    print(str(data))
    d.putData(sql="INSERT INTO aom_task_before (taskdate,tasktype,userid,taskstatus,taskcontent) VALUES (NOW(),'installsoftware',1,1,\"%s\")" %(pymysql.escape_string(str(data))))
    d.putData(sql="insert into aom_task_soft (taskid,softTYPEID)values (%s,%s)"%(d.getLaseID(),request.POST.get('softversion',1)))
    d.commit()
    d.close()
    return HttpResponseRedirect("/aom/installsoftlist/")   

    
#安装软件列表相信信息
def installsoftinfo(request):
    if request.method != "GET":
        return HttpResponse("参数错误")
    data=_initPage(request)
    dbcon=db.opMysqlObj(**{'dbname':'default'})
    sql="SELECT a.taskid,a.taskdate,f.`softname`,f.`softversion`,c.`username`,d.`taskstatusname` FROM (SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_before WHERE tasktype='installsoftware' UNION ALL SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_after WHERE tasktype='installsoftware')  a LEFT JOIN aom_task_type b ON a.tasktype=b.tasktypeid LEFT JOIN auth_user c ON a.userid=c.`id` LEFT JOIN aom_task_status d ON a.taskstatus=d.`taskstatusid` LEFT JOIN aom_task_soft e ON a.taskid=e.`taskid` LEFT JOIN aom_softtype f ON  e.`softtypeid`=f.`softtypeid` where a.taskid="+request.GET.get('taskid',1)+" order by a.taskid desc"
    data['taskinfohead']=['任务ID','任务日期','软件名','软件版本','用户','状态']
    data['taskinfo']=dbcon.getData(**{'sql':sql})
    
    sql='''select msgid,msgdate,REPLACE(REPLACE(msgcontent,'\n','<br>'),' ','&nbsp&nbsp')  from aom_msg where taskid='''+request.GET.get('taskid',1)
    objects, page_range = _my_pagination(request, dbcon.getData(**{'sql':sql}))
    objects_head=['消息id','消息日期','消息内容']
    data['objects']=objects
    data['page_range']=page_range
    data['objects_head']=objects_head
    return render(request, 'aom/installsoftinfo.html',data) 

@csrf_exempt    
def postData(request):
    if request.method != "POST":
        return HttpResponse("参数错误")
    #print(request.POST.get('softversion'))
    return_json={'result':'error'}
    if request.POST.get('page')=='installjdkadd':
        if request.POST.get('type')=='defautlpath':    
            return_json = {'result':{'defaultpath':_getDefaultpath(request.POST.get('softversion'))}}   
    #print(return_json)            
    return HttpResponse(json.dumps(return_json), content_type='application/json')        

def _getDefaultpath(softtypeid):
    dbcon=db.opMysqlObj(**{'dbname':'default'})
    return(dbcon.getDefaultPath(**{'softtypeid':softtypeid}))
    
def test1(request):
    return render(request, 'aom/head.html',{})