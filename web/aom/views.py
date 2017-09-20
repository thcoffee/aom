from django.shortcuts import render
from django.db import connections,transaction
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
import pymysql
# Create your views here.

class opDatabaseObj(object):
    def __init__(self,**kwages):
        self.databases=kwages['dbname']
        self._getdb()
        pass
        
    def _getdb(self):
        temp=settings.DATABASES[self.databases]
        temp2={}
        temp2['user'],temp2['password'],temp2['host'],temp2['database'],temp2['port']=temp['USER'],temp['PASSWORD'],temp['HOST'],temp['NAME'],int(temp['PORT'])
        temp2['charset']='utf8'
        self.db=pymysql.connect(**temp2)
    
    def getLaseID(self):
        
        return(self.getData('SELECT LAST_INSERT_ID()')[0][0])
    
    def getData(self,sql):
        cur=self.db.cursor()
        cur.execute('SELECT LAST_INSERT_ID()')
        return(cur.fetchall())
        
    def commit(self):
        self.db.commit()    
        
    def putData(self,sql):
        print(sql)
        cur=self.db.cursor() 
        cur.execute(sql)
    
def _getdb(**kwages):
    temp=settings.DATABASES[kwages['dbname']]
    temp2={}
    temp2['user'],temp2['password'],temp2['host'],temp2['database'],temp2['port']=temp['USER'],temp['PASSWORD'],temp['HOST'],temp['NAME'],int(temp['PORT'])
    temp2['charset']='utf8'
    db=pymysql.connect(**temp2)
    return(db)
    
def _getData(**kwages):
    #cur = connections[kwages['dbname']].cursor()
    db=_getdb(**kwages)
    cur=db.cursor() 
    cur.execute(kwages['sql'])
    db.close()
    return(cur.fetchall())

def _putData(**kwages):
    #cur = connections[kwages['dbname']].cursor()
    db=_getdb(**kwages)
    cur=db.cursor() 
    for i in kwages['sqls']:
        cur.execute(i)
    db.commit()
    #cur.close()
    #db.close()
    cur.execute('SELECT LAST_INSERT_ID()')
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
def installsoftList(request):
    data=_initPage(request)
    sql='''SELECT a.taskid,a.taskdate,f.`softname`,f.`softversion`,c.`username`,d.`taskstatusname` FROM
(SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_before WHERE tasktype='installsoftware' UNION ALL 
SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_after WHERE tasktype='installsoftware')  a LEFT JOIN aom_task_type b ON a.tasktype=b.tasktypeid
LEFT JOIN auth_user c ON a.userid=c.`id` LEFT JOIN aom_task_status d ON a.taskstatus=d.`taskstatusid`
LEFT JOIN aom_task_soft e ON a.taskid=e.`taskid` LEFT JOIN aom_softtype f ON  e.`softtypeid`=f.`softtypeid`
 ORDER BY a.taskid DESC'''

    objects, page_range = _my_pagination(request, _getData(**{'dbname':'default','sql':sql}))
    objects_head=['任务ID','任务日期','软件名','软件版本','用户','状态']
    data['objects']=objects
    data['page_range']=page_range
    data['objects_head']=objects_head
    return render(request, 'aom/installsoftlist.html',data)

def installjdkAdd(request):
    data=_initPage(request)
    sql="SELECT softtypeid,softname,softversion FROM aom_softtype where softname='jdk' ORDER BY 2,3;"
    data['softinfo']= _getData(**{'dbname':'default','sql':sql})
    return render(request, 'aom/installjdkadd.html',data) 

def jdkcommit(request):
    if request.method != "POST":
        return HttpResponse('''参数错误''')
    sql="SELECT softfiles FROM aom_softtype where softTYPEID="+request.POST.get('softversion',1)
    data={'task':'installsoftware',
          'localpath':_getData(**{'dbname':'default','sql':sql})[0][0],
          'remotepath':request.POST.get('remotepath',''),
          'name':'jdk','node':request.POST.getlist('node')}
    print(data)
    d=opDatabaseObj(**{'dbname':'default'})
    d.putData("INSERT INTO aom_task_before (taskdate,tasktype,userid,taskstatus,taskcontent) VALUES (NOW(),'installsoftware',1,1,\"%s\")" %(str(data)))
    d.putData("insert into aom_task_soft (taskid,softTYPEID)values (%s,%s)"%(d.getLaseID(),request.POST.get('softversion',1)))
    d.commit()
    return HttpResponseRedirect("/aom/installsoftlist/")  

def installsoftinfo(request):
    if request.method != "GET":
        return HttpResponse('''参数错误''')
    data=_initPage(request)
    sql="SELECT a.taskid,a.taskdate,f.`softname`,f.`softversion`,c.`username`,d.`taskstatusname` FROM (SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_before WHERE tasktype='installsoftware' UNION ALL SELECT taskid,taskdate,tasktype,userid,taskstatus FROM aom_task_after WHERE tasktype='installsoftware')  a LEFT JOIN aom_task_type b ON a.tasktype=b.tasktypeid LEFT JOIN auth_user c ON a.userid=c.`id` LEFT JOIN aom_task_status d ON a.taskstatus=d.`taskstatusid` LEFT JOIN aom_task_soft e ON a.taskid=e.`taskid` LEFT JOIN aom_softtype f ON  e.`softtypeid`=f.`softtypeid` where a.taskid="+request.GET.get('taskid',1)+" order by a.taskid desc"
    data['taskinfohead']=['任务ID','任务日期','软件名','软件版本','用户','状态']
    data['taskinfo']=_getData(**{'dbname':'default','sql':sql})
    sql='''select msgid,msgdate,msgcontent  from aom_msg where taskid='''+request.GET.get('taskid',1)
    objects, page_range = _my_pagination(request, _getData(**{'dbname':'default','sql':sql}))
    objects_head=['消息id','消息日期','消息内容']
    data['objects']=objects
    data['page_range']=page_range
    data['objects_head']=objects_head
    
    
    return render(request, 'aom/installsoftinfo.html',data) 
def test1(request):
    return render(request, 'aom/head.html',{})