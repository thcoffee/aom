from django.shortcuts import render
from django.db import connections,transaction
from django.core.paginator import Paginator
# Create your views here.

def _getData(sql):
    cur = connections['zsj'].cursor()
    cur.execute(sql)
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
    
def test(request):
    sql1=[]
    sql1.append('select * from adc_deploy order by 1 limit 0,121')
    objects, page_range = _my_pagination(request, _getData(''.join(sql1)))
    objects_head=['字段1','字段2','字段3','字段4','字段5','字段6']
    data={'objects':objects,'page_range':page_range,'objects_head':objects_head}
    return render(request, 'aom/test.html',data)