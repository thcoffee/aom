import sys,os,time
import threading
import logging
import traceback
import pymysql

from functions import test1

stdLogger = logging.getLogger('root')

class taskThreadObj(threading.Thread):            
    
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
            self.processTask()
            time.sleep(5)
        
    def processTask(self):
        db=pymysql.connect(**self.dbcon)
        cur=db.cursor() 
        cur.execute("select * from aom_task_before where taskstatus=1 for update")
        data=cur.fetchall()
        for i in data:
            if i['tasktype']==u'test1':
                cur.execute('update aom_task_before set taskstatus=2 where taskid=%s'%(i['taskid']))
                db.commit()
                stdLogger.debug("".join([self.name,str(i)]))                    
                self.systemDict['thread']['task'][self.name]['taskId']=i['taskid']
                t=test1.test1(**i)
                t.run() 
                stdLogger.debug("".join([self.name,' ',str(i['taskid']),' Processed.']))
                self.systemDict['thread']['task'][self.name]['taskId']=None
                break
                
                   
        cur.close()
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

            
