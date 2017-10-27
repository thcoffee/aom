# -*- coding: utf-8 -*-
import sys,os,time
import threading
import logging
import traceback
import pymysql

from functions import test1
from functions import installSoftWare
from functions import db as dbO
from functions import syncConf
stdLogger = logging.getLogger('root')

#任务线程
class taskThreadObj(threading.Thread):            
    #构造方法
    def __init__(self,**kwages):
        threading.Thread.__init__(self)
        self.systemDict=kwages['systemDict']
        self.baseParams=kwages['baseParams']
        self.threadList=kwages['threadList']
        self.name=kwages['name']
        self.taskId=None
        self.dbcon=self.baseParams['dbcon']
        self.daemon = True
        self.start()
      
    def run(self):
        try:
            self._run()
        except Exception as info:
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread '+self.name+' collapse')

            
    def _run(self):
        stdLogger.info('The thread '+self.name+' Start to finish')
        while 1:
            if self.systemDict['main']['target']=='off': 
                stdLogger.info(self.name+' thread has stopped.')
                break
            try:
                self.processTask()
            except Exception as info:
                self.systemDict['thread']['task'][self.name]['taskId']=None
                stdLogger.error(traceback.format_exc())
            time.sleep(5)
            
    #获取任务
    def _getTask(self,**kwages):
        db=kwages['db']
        data=db.getData(sql="select * from aom_task_before where taskstatus=1 for update")   
        for i in data:
            if 1 == 1:
                db.putData(sql='update aom_task_before set taskstatus=2 where taskid=%s'%(i['taskid']))
                db.commit()
                return({'status':True,'obj':i})
        db.commit()        
        return({'status':False})
        
    #处理任务
    def processTask(self):
        db=dbO.opMysqlObj(**self.dbcon) 
        taskInfo=self._getTask(**{'db':db})        
        if taskInfo['status']:
            i=taskInfo['obj']
            i['db']=db
            stdLogger.info(" ".join([self.name,str(i['taskid']),' begin.']))                    
            self.systemDict['thread']['task'][self.name]['taskId']=i['taskid']
            taskDict=eval(i['taskcontent'])
            if i['tasktype']==u'test1':
                t=test1.test1(**i)
                t.run() 
            elif i['tasktype']==u'syncnginxconf':
                t=syncConf.syncNginxConf(**i)
                t.run()
            elif i['tasktype']==u'installsoftware':
                if taskDict['name']=='jdk':
                    t=installSoftWare.jdk(**i)
                    t.install()
                elif taskDict['name']=='nginx':
                    t=installSoftWare.nginx(**i)
                    t.install()
                elif taskDict['name']=='tomcat':
                    t=installSoftWare.tomcat(**i)
                    t.install()
                else:
                    db.putData(sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),1,'%s',%s)" %("不支持该软件安装.",i['taskid']))
            else:
                db.putData(sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),1,'%s',%s)" %("未知的任务类型.",i['taskid']))  
            db.putData(sql='update aom_task_before set taskstatus=3 where taskid=%s'%(i['taskid']))
            db.putData(sql='insert into aom_task_after select * from aom_task_before where taskid=%s'%(i['taskid']))
            db.putData(sql='delete from aom_task_before where taskid=%s'%(i['taskid']))
            db.commit()
            self.systemDict['thread']['task'][self.name]['taskId']=None
            stdLogger.info("".join([self.name,' ',str(i['taskid']),' Processed.']))     
        db.commit()                
        db.close()
    

        
class taskThreadStartObj(threading.Thread):
    
    def __init__(self,**kwages):
        threading.Thread.__init__(self)
        self.systemDict=kwages['systemDict']
        self.baseParams=kwages['baseParams']
        self.threadList=kwages['threadList']
        self.dbcon=self.baseParams['dbcon']
        self.daemon = True
        self.start()
        pass
        
    def run(self):
        try:
            self._run()  
        except Exception as info:
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread task collapse')
            
    def _run(self):
        #stdLogger.error('The thread task Start to finish')
        self.threadList['task']={}
        self.systemDict['thread']['task']={} 
        for i in range(3):
            
            self.threadList['task']['task'+str(i)]=taskThreadObj(**{'threadList':self.threadList,
                                                            'systemDict':self.systemDict,
                                                            'baseParams':self.baseParams,
                                                            'name':'task'+str(i)})                                                    
            self.systemDict['thread']['task']['task'+str(i)]={}

            
