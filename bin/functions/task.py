import sys,os,time
import threading
import logging
import traceback
import pymysql
#from functions import test1

stdLogger = logging.getLogger('root')

class taskThreadObj(threading.Thread):            
    
    def __init__(self,**kwages):
        threading.Thread.__init__(self)
        self.systemDict=kwages['systemDict']
        self.baseParams=kwages['baseParams']
        self.threadList=kwages['threadList']
        self.name=kwages['name']
        self.dbcon=self.baseParams['dbcon']
        self.daemon = True
        self.start()
    
    def _connect(self):
        try:
            self.db=pymysql.connect(**self.dbcon)
            return(True)
        except Exception as info:
            stdLogger.error(traceback.format_exc())         
            return(False)
    
    def run(self):
        try:
            self._run()
        except Exception as info:
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread '+self.name+' collapse')

            
    def _run(self):
        stdLogger.error('The thread '+self.name+' Start to finish')
        while 1:
            if self.systemDict['main']['target']=='off': 
                stdLogger.info(self.name+' thread has stopped.')
                break
            if self._connect():
                cur=self.db.cursor() 
                cur.execute('select * from aom_custom')
                stdLogger.debug(cur.fetchall())
            time.sleep(5)
            
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
        stdLogger.error('The thread task Start to finish')
        for i in range(3):
            self.threadList['task'+str(i)]=taskThreadObj(**{'threadList':self.threadList,
                                                            'systemDict':self.systemDict,
                                                            'baseParams':self.baseParams,
                                                            'name':'task'+str(i)})
            self.systemDict['thread']['task'+str(i)]={}

            
