import sys,os,time
import threading
import yaml
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
            self.systemDict['thread']['task']['switch']['state']='off'
            
    def _run(self):
        while 1:
            if self.systemDict['thread']['task']['switch']['target']=='off':
                self.systemDict['thread']['task']['switch']['state']='off'
                stdLogger.info('The thread task has stopped.')
                break
            db=pymysql.connect(**self.dbcon)
            cur=db.cursor() 
            cur.execute('select * from aom_custom')
            stdLogger.debug(cur.fetchall())
            test1.ddd()
            time.sleep(5)