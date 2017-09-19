from django.shortcuts import render
from django.db import connections,transaction
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.

def _getData(**kwages):
    cur = connections[kwages['dbname']].cursor()
    cur.execute(kwages['sql'])
    return(cur.fetchall())
    
def _my_pagination(request, queryset, display_amount=10, after_range_num = 3,bevor_range_num = 2):
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

def _initPage(request):
    data={}
    data['userid']=str(request.user)
    return(data)
    
@login_required(login_url="/admin/login/")      
def test(request):
    data=_initPage(request)
    sql1=[]
    sql1.append('select * from adc_deploy order by 1 limit 0,121')
    objects, page_range = _my_pagination(request, _getData(**{'dbname':'zsj','sql':''.join(sql1)}))
    objects_head=['字段1','字段2','字段3','字段4','字段5','字段6']
    data['objects']=objects
    data['page_range']=page_range
    data['objects_head']=objects_head
    return render(request, 'aom/test.html',data)

@login_required(login_url="/admin/login/")   
def installsoftwareList(request):
    data=_initPage(request)
    sql='''SELECT a.taskid,a.taskdate,b.`tasktypecname`,c.`username`,d.`taskstatusname` FROM
(SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_before WHERE tasktype='installsoftware' UNION ALL 
SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_after WHERE tasktype='installsoftware')  a LEFT JOIN aom_task_type b ON a.tasktype=b.tasktypeid
LEFT JOIN auth_user c ON a.userid=c.`id` LEFT JOIN aom_task_status d ON a.taskstatus=d.`taskstatusid` order by a.taskid desc'''

    objects, page_range = _my_pagination(request, _getData(**{'dbname':'default','sql':sql}))
    objects_head=['任务ID','任务日期','任务类型','用户','状态']
    data['objects']=objects
    data['page_range']=page_range
    data['objects_head']=objects_head
    return render(request, 'aom/installsoftwarelist.html',data)

def installsoftwareAdd(request):
    data=_initPage(request)
    return render(request, 'aom/installsoftwareadd.html',data) 

def jdkcommit(request):
    if request.method != "POST":
        return HttpResponse('''参数错误''')
    #print(request.POST.get('remotepath',1))
    #print(request.POST.get('localpath',1))
    #print(request.POST.getlist('usertype'))
    #for i in request.POST:
    #    print(i,request.POST.get(i,1))
    data={'task':'installsoftware','localpath':request.POST.get('localpath',1),'remotepath':request.POST.get('remotepath',1),'name':'jdk','node':request.POST.getlist('usertype')}
    print(data)    
    return HttpResponseRedirect("/aom/installsoftwarelist/")  

def installsoftwareinfo(request):
    if request.method != "GET":
        return HttpResponse('''参数错误''')
    data=_initPage(request)
    sql='''select msgid,msgdate,msgcontent  from aom_msg where taskid='''+request.GET.get('taskid',1)
    print(sql)
    print(_getData(**{'dbname':'default','sql':sql}))
    objects, page_range = _my_pagination(request, _getData(**{'dbname':'default','sql':sql}))
    objects_head=['消息id','消息日期','消息内容']
    data['objects']=objects
    data['page_range']=page_range
    data['objects_head']=objects_head
    
    
    return render(request, 'aom/installsoftwareinfo.html',data) 
def test1(request):
    return render(request, 'aom/head.html',{})